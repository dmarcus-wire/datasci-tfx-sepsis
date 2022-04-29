# DAG base image

We are using the s2i base image and process to build a
base image that will have the requirements needed for the dag to run.

Base Image: python-3.8-ubi8:latest

## Technical Notes
```
# build dag image
oc new-build https://github.com/redhat-na-ssa/mlops-prototype#airflow-container --context-dir=dag-image
```