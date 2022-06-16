# Serve Model

The model is served through an API using Flask.

Example request to the model:

```bash
curl -X POST -H "Content-Type: application/json" --data '{"hr":43.2, "resp": 32.1, "temp": 98.2}' http://mlops-prototype-my-model-server.apps.cluster-cghmd.cghmd.sandbox879.opentlc.com/predictions
```

## Why

"Because no app is an island. No app provides business value on its own—at least not for very long. Apps must be connected to your existing and future technology investments to provide continuous value and to actually exist as a part of your business. APIs give you a standard way of integrating everything—without the need to rebuild it all every time you introduce something new."

[Source](https://www.redhat.com/en/topics/api/why-choose-red-hat-apis#:~:text=Red%20Hat%20gives%20your%20business,new%E2%80%94even%20as%20you%20grow)

## Deploy API

The source code to deploy the model through an API with Flask exists in the [app](https://github.com/redhat-na-ssa/mlops-prototype/tree/main/app) folder of the repository. The Flask app is built using S2I:

"Source-to-Image (S2I) is a toolkit and workflow for building reproducible container images from source code. S2I produces ready-to-run images by injecting source code into a container image and letting the container prepare that source code for execution. By creating self-assembling builder images, you can version and control your build environments exactly like you use container images to version your runtime environments." ~[Source](https://github.com/openshift/source-to-image)

To build the app manually, run:

```bash
oc new-app --image-stream=python:3.8-ubi8 --context-dir=/app --env=GUNICORN_CMD_ARGS="--bind=0.0.0.0:8080" https://github.com/redhat-na-ssa/mlops-prototype.git
```

## Other Serving Options

1. TFX `BulkInferrer` component

    This is demonstrated in the Demonstrated in [vitals-septic-prediction-pipeline.ipynb](https://github.com/redhat-na-ssa/mlops-prototype/blob/main/notebooks/vitals-septic-prediction-pipeline.ipynb), this component performs in micro-batch in-memory model inference and remote inference on unlabeled TF examples.

2. Intel OpenVino Operator

    The Operator installs and manages development tools and production AI deployments in an OpenShift cluster. It enables easy deployment and management of AI inference services by creating `ModelServer` resource.

    The Operator also integrates with the JupyterHub `Spawner` in `Red Hat OpenShift Data Science` and `Open Data Hub`.

    [Source](https://docs.openvino.ai/latest/ovms_extras_openvino-operator-openshift-readme.html?highlight=openshift)

3. Seldon Operator

    Seldon Core, our open-source framework, makes it easier and faster to deploy your machine learning models and experiments at scale on Kubernetes. Serve your models built in any open-source or commercial model building framework. Leverage powerful Kubernetes features like Custom Resource Definitions to manage model graphs. And connect your continuous integration and deployment (CI/CD) tools to scale and update your deployment.

    [Source](https://catalog.redhat.com/software/operators/detail/5ec3fa5778e79e6a879fa213)
