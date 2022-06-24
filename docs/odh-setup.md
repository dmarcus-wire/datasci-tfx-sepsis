# ODH Setup

## Uses

## Instructions

Install ODH on OpenShift 

```yaml
apiVersion: kfdef.apps.kubeflow.org/v1
kind: KfDef
metadata:
  name: opendatahub
  namespace: sepsis-detection
spec:
  applications:
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: odh-common
    name: odh-common
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: odhseldon/cluster
    name: odhseldon
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: superset
    name: superset
  - kustomizeConfig:
      parameters:
      - name: namespace
        value: openshift-operators
      repoRef:
        name: manifests
        path: kafka/cluster
    name: strimzi-operator
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: kafka/kafka
    name: kafka-cluster
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: grafana/cluster
    name: grafana-cluster
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: grafana/grafana
    name: grafana-instance
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: radanalyticsio/spark/cluster
    name: radanalyticsio-spark-cluster
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: prometheus/cluster
    name: prometheus-cluster
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: prometheus/operator
    name: prometheus-operator
  - kustomizeConfig:
      parameters:
        - name: s3_endpoint_url
          value: "s3.odh.com"
      repoRef:
        name: manifests
        path: jupyterhub/jupyterhub
    name: jupyterhub
  - kustomizeConfig:
      overlays:
      #- cuda-11.0.3
      - additional
      repoRef:
        name: manifests
        path: jupyterhub/notebook-images
    name: notebook-images
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: odhargo/cluster
    name: odhargo-cluster
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: odhargo/odhargo
    name: odhargo
  - kustomizeConfig:
      repoRef:
        name: manifests
        path: odh-dashboard
    name: odh-dashboard
  repos:
  - name: kf-manifests
    uri: https://github.com/kubeflow/manifests/archive/v1.2-branch.tar.gz
  - name: manifests
    uri: https://github.com/opendatahub-io/odh-manifests/tarball/master
  version: master
```


```
# install ODH on OpenShift using the kfdef below
docs/opendatahub-kfdef

# git clone the project
git clone https://github.com/redhat-na-ssa/mlops-prototype.git

## launch terminal and run setup script from the directory the setup.sh script
./setup.sh

# start at the notebooks/vitals-septic-prediction-pipeline.ipynb
Launch vitals-septic-prediction-pipeline.ipynb

## launch terminal and run cleanup script from the directory the cleanup.sh script
# ./cleanup.sh

## Airflow configuration in Airflow subdir

## ODH Uninstallation
# Option: delete ALL resources labeled with "opendatahub" clusterwide
oc delete all --selector opendatahub.io/component=true --all-namespaces
oc delete operatorgroup -n openshift-operators opendatahub

# Option: delete ONLY the project
oc delete project <project-name>

# Option: delete ONLY the kfdef in the project requires the file path
oc delete -f <path>/kfdef
```