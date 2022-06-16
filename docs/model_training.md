# Automate Model Training

We created a TensorFlow model using a TFX pipeline which covers every step in an end-to-end machine learning pipeline, from data ingestion to pushing a model to serving. To automate the retraining of this model, we deployed Apache Airflow.

## Deploy Airflow on OpenShift

Airflow is deployed on OpenShift using a Helm chart. Community instructions are available [here](https://github.com/redhat-na-ssa/airflow-on-openshift).

## Model Training

With the TFX Trainer component, we trained the model in  a standardized model format. Allows us to parameterize our training and evaluation arguments, such as the number of steps as shown in the example. Inherit the benefits of using TensorFlow for accelerating our model training, such as the TF distribute APIs, for distributing training across multiple cores and machines.

[Source](https://www.tensorflow.org/tfx/guide/trainer)
[Source](https://github.com/dmarcus-wire/tfx-pipelines/tree/main/components#trainer)

## Model Evaluation

model performance evaluation as inputs
will use the model created by the trainer and the original input data artifact
many teams would write custom evaluation code that was buggy and hard to maintain with a lot of duplication and made it hard to replicate
assured that your pipeline will only graduate a model to production when it has exceeded the performance of previous models

[Source](https://www.tensorflow.org/tfx/guide/evaluator)

[Source](https://github.com/dmarcus-wire/tfx-pipelines/tree/main/components#trainer)
