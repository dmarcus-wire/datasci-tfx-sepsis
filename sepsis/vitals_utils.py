from typing import List, Text

from absl import logging

import tensorflow as tf
import tensorflow_transform as tft

from tfx import v1 as tfx
from tfx_bsl.public import tfxio
from tensorflow_transform import TFTransformOutput

_BATCH_SIZE = 40

NUMERICAL_FEATURES = ['HR', 'Resp', 'Temp']

# Keys
LABEL_KEY = 'isSepsis'


def t_name(key):
  """
  Rename the feature keys so that they don't clash with the raw keys when
  running the Evaluator component.
  Args:
    key: The original feature key
  Returns:
    key with '_xf' appended
  """
  return key + '_xf'

def _input_fn(file_pattern: List[Text],
              data_accessor: tfx.components.DataAccessor,
              tf_transform_output: tft.TFTransformOutput,
              batch_size: int = 200) -> tf.data.Dataset:
  """Generates features and label for tuning/training.
  Args:
    file_pattern: List of paths or patterns of input tfrecord files.
    data_accessor: DataAccessor for converting input to RecordBatch.
    tf_transform_output: A TFTransformOutput.
    batch_size: representing the number of consecutive elements of returned
      dataset to combine in a single batch
  Returns:
    A dataset that contains (features, indices) tuple where features is a
      dictionary of Tensors, and indices is a single Tensor of label indices.
  """
  return data_accessor.tf_dataset_factory(
      file_pattern,
      tfxio.TensorFlowDatasetOptions(
          batch_size=batch_size, label_key=LABEL_KEY),
      tf_transform_output.transformed_metadata.schema)

def _get_tf_examples_serving_signature(model, tf_transform_output):
  """Returns a serving signature that accepts `tensorflow.Example`."""

  # We need to track the layers in the model in order to save it.
  # TODO(b/162357359): Revise once the bug is resolved.
  model.tft_layer_inference = tf_transform_output.transform_features_layer()

  @tf.function(input_signature=[
      tf.TensorSpec(shape=[None], dtype=tf.string, name='examples')
  ])
  def serve_tf_examples_fn(serialized_tf_example):
    """Returns the output to be used in the serving signature."""
    raw_feature_spec = tf_transform_output.raw_feature_spec()
    # Remove label feature since these will not be present at serving time.
    raw_feature_spec.pop(LABEL_KEY)
    raw_features = tf.io.parse_example(serialized_tf_example, raw_feature_spec)
    transformed_features = model.tft_layer_inference(raw_features)
    logging.info('serve_transformed_features = %s', transformed_features)

    outputs = model(transformed_features)
    # TODO(b/154085620): Convert the predicted labels from the model using a
    # reverse-lookup (opposite of transform.py).
    return {'outputs': outputs}

  return serve_tf_examples_fn


def _get_transform_features_signature(model, tf_transform_output):
  """Returns a serving signature that applies tf.Transform to features."""

  # We need to track the layers in the model in order to save it.
  # TODO(b/162357359): Revise once the bug is resolved.
  model.tft_layer_eval = tf_transform_output.transform_features_layer()

  @tf.function(input_signature=[
      tf.TensorSpec(shape=[None], dtype=tf.string, name='examples')
  ])
  def transform_features_fn(serialized_tf_example):
    """Returns the transformed_features to be fed as input to evaluator."""
    raw_feature_spec = tf_transform_output.raw_feature_spec()
    raw_features = tf.io.parse_example(serialized_tf_example, raw_feature_spec)
    transformed_features = model.tft_layer_eval(raw_features)
    logging.info('eval_transformed_features = %s', transformed_features)
    return transformed_features

  return transform_features_fn


def export_serving_model(tf_transform_output, model, output_dir):
  """Exports a keras model for serving.
  Args:
    tf_transform_output: Wrapper around output of tf.Transform.
    model: A keras model to export for serving.
    output_dir: A directory where the model will be exported to.
  """
  # The layer has to be saved to the model for keras tracking purpases.
  model.tft_layer = tf_transform_output.transform_features_layer()

  signatures = {
      'serving_default':
          _get_tf_examples_serving_signature(model, tf_transform_output),
      'transform_features':
          _get_transform_features_signature(model, tf_transform_output),
  }

  model.save(output_dir, save_format='tf', signatures=signatures)


def _build_keras_model(tf_transform_output: TFTransformOutput
                       ) -> tf.keras.Model:
  """Creates a DNN Keras model for classifying vitals data.
  Args:
    tf_transform_output: [TFTransformOutput], the outputs from Transform
  Returns:
    A keras Model.
  """
  feature_spec = tf_transform_output.transformed_feature_spec().copy()
  feature_spec.pop(LABEL_KEY)

  inputs = {}
  for key, spec in feature_spec.items():
    if isinstance(spec, tf.io.VarLenFeature):
      inputs[key] = tf.keras.layers.Input(
          shape=[None], name=key, dtype=spec.dtype, sparse=True)
    elif isinstance(spec, tf.io.FixedLenFeature):
      # TODO(b/208879020): Move into schema such that spec.shape is [1] and not
      # [] for scalars.
      inputs[key] = tf.keras.layers.Input(
          shape=spec.shape or [1], name=key, dtype=spec.dtype)
    else:
      raise ValueError('Spec type is not supported: ', key, spec)

  output = tf.keras.layers.Concatenate()(tf.nest.flatten(inputs))
  output = tf.keras.layers.Dense(100, activation='relu')(output)
  output = tf.keras.layers.Dense(70, activation='relu')(output)
  output = tf.keras.layers.Dense(50, activation='relu')(output)
  output = tf.keras.layers.Dense(20, activation='relu')(output)
  output = tf.keras.layers.Dense(1)(output)
  return tf.keras.Model(inputs=inputs, outputs=output)


# TFX Trainer will call this function.
def run_fn(fn_args: tfx.components.FnArgs):
  """Train the model based on given args.
  Args:
    fn_args: Holds args used to train the model as name/value pairs.
  """
  tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

  train_dataset = _input_fn(fn_args.train_files, fn_args.data_accessor,
                            tf_transform_output, _BATCH_SIZE)
  eval_dataset = _input_fn(fn_args.eval_files, fn_args.data_accessor,
                           tf_transform_output, _BATCH_SIZE)

  model = _build_keras_model(tf_transform_output)

  model.compile(
      loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
      optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
      metrics=[tf.keras.metrics.BinaryAccuracy()])

  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=fn_args.model_run_dir, update_freq='batch')

  model.fit(
      train_dataset,
      steps_per_epoch=fn_args.train_steps,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps,
      callbacks=[tensorboard_callback])

  # Export the model.
  export_serving_model(tf_transform_output, model, fn_args.serving_model_dir)


def _fill_in_missing(x):
  """Replace missing values in a SparseTensor.
  Fills in missing values of `x` with '' or 0, and converts to a dense tensor.
  Args:
    x: A `SparseTensor` of rank 2.  Its dense shape should have size at most 1
      in the second dimension.
  Returns:
    A rank 1 tensor where missing values of `x` have been filled in.
  """
  if not isinstance(x, tf.sparse.SparseTensor):
    return x

  default_value = '' if x.dtype == tf.string else 0
  return tf.squeeze(
      tf.sparse.to_dense(
          tf.SparseTensor(x.indices, x.values, [x.dense_shape[0], 1]),
          default_value),
      axis=1)


def preprocessing_fn(inputs):
  """tf.transform's callback function for preprocessing inputs.
  Args:
    inputs: map from feature keys to raw not-yet-transformed features.
  Returns:
    Map from string feature key to transformed feature operations.
  """
  outputs = {}
  for key in NUMERICAL_FEATURES:
    # If sparse make it dense, setting nan's to 0 or '', and apply zscore.
    outputs[t_name(key)] = tft.scale_to_z_score(
        _fill_in_missing(inputs[key]), name=key)

  outputs[LABEL_KEY] = _fill_in_missing(inputs[LABEL_KEY])

  return outputs