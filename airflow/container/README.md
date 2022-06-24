# DAG base image

We are using the s2i base image and process to build a
base image that will have the requirements needed for the dag to run.

Base Image: python-3.8-ubi8:latest

## Quickstart

```bash
# build dag image
oc new-build \
  https://github.com/redhat-na-ssa/mlops-prototype \
  --name=dag-runner \
  --image-stream=openshift/python:3.8-ubi8 \
  --context-dir=airflow/container
```

## Technical Notes

- Issues between the official airflow container (Debian 10.11) and UBI may exist
  - There be dragons here due to debian based image
- Official airflow container is running Python 3.7 currently
- Using the official airflow image can save time
  - Use a virtualenv DAG with pip install for requirements (this will be slower when starting dag jobs; you can mount a PVC with cached files to speed up some)
- Could build our own airflow using UBI
- Could make official airflow image into s2i compatable or patching with all the requirements
- This is for SCIENCE - it was a fun exercise to see what was possible
- Some options:
  - Build UBI image with airflow
  - Find good practices for using official image in openshift
    - Identify / submit upstream patches
    - Identify limitations
