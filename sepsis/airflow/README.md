# Deploy Airflow on OpenShift
oc new-project airflow

# Change to project airflow
oc project airflow

# Install Helm Chart
helm repo add apache-airflow https://airflow.apache.org && helm repo update

# Deploy Airflow
helm install airflow apache-airflow/airflow \
    --set webserver.defaultUser.password=RedHat123! \
    --set dags.gitSync.repo=https://github.com/redhat-na-ssa/mlops-prototype \
    --set dags.gitSync.branch=main \
    --set dags.gitSync.subPath=workflows/dags
