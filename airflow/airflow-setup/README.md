# Airflow setup procedure for OpenShift

```
# git clone project
git clone https://github.com/redhat-na-ssa/mlops-prototype.git

# login to OpenShift cluster via CLI with admin permissions
oc login <token>

# create a namespace using the create-namespace.yml file
oc create -f create-namespace.yaml

# enter new 'airflow' project
oc project airflow

# add the helm repo for airflow to your project
helm repo add apache-airflow https://airflow.apache.org

# get the airflow chart
helm pull apache-airflow/airflow

# unpack the tar file
tar xzf airflow-<version>.tgz

# copy the airflow-values.yaml file over the airflow/values.yaml file
cp airflow-values.yaml airflow/values.yaml

# copy the charts-postgresql-values.yaml file over the airflow/charts/postgresql/values.yaml
cp charts-postgresql-values.yaml airflow/charts/postgresql/values.yaml

# move into the airflow folder and install the helm chart specifying a path to the stored/to-be-stored DAGs
cd airflow && helm upgrade --install airflow ./ --namespace airflow \
--values ./values.yaml \
--set dags.gitSync.repo=https://github.com/redhat-na-ssa/mlops-prototype.git \
--set dags.gitSync.branch=main \
--set dags.gitSync.subPath=airflow/workflows/dags

# create a route #1
# name airflow-webserver
# service airflow-webserver
# target port 8080-8080 TCP
# TLS termination Edge
# Insecure Traffic Redirect

oc expose svc/airflow-webserver

oc create route edge \
  --service=airflow-webserver \
  --insecure-policy=Redirect \
  --port=8080

# create a route #1
# name airflow-flower
# service airflow-flower
# target port 5555-5555
# TLS termination Edge
# Insecure Traffic Redirect

oc create route edge \
  --service=airflow-flower \
  --insecure-policy=Redirect \
  --port=5555
```

# References
Steps originate from https://github.com/davwhite/airflow-helm and https://dsri.maastrichtuniversity.nl/docs/workflows-airflow/