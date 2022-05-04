# DAG base image

We are using the s2i base image and process to build a
base image that will have the requirements needed for the dag to run.

Base Image: python-3.8-ubi8:latest

## Quickstart
```
# build dag image
oc new-build https://github.com/redhat-na-ssa/mlops-prototype#airflow-container \
  --name=dag-runner \
  --context-dir=airflow/container \
  --source-image=openshift/python-3.8-ubi8
```

## Technical Notes
