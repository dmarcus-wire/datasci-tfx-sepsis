
import tensorflow as tf
import tensorflow_transform as tft

# Imported files such as vitals_constants are normally cached, so changes are
# not honored after the first import.  Normally this is good for efficiency, but
# during development when we may be iterating code it can be a problem. To
# avoid this problem during development, reload the file.
import vitals_constants
import sys
import importlib
importlib.reload(vitals_constants)

_NUMERICAL_FEATURES = vitals_constants.NUMERICAL_FEATURES
_LABEL_KEY = vitals_constants.LABEL_KEY


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
  for key in _NUMERICAL_FEATURES:
    # If sparse make it dense, setting nan's to 0 or '', and apply zscore.
    outputs[vitals_constants.t_name(key)] = tft.scale_to_z_score(
        _fill_in_missing(inputs[key]), name=key)

  outputs[_LABEL_KEY] = _fill_in_missing(inputs[_LABEL_KEY]) 
    
  return outputs
