# Deploy Airflow on OpenShift
oc new-project airflow

# Change to project airflow
oc project airflow

# Install Helm Chart
helm repo add apache-airflow https://airflow.apache.org && helm repo update

# Deploy Airflow, change password and subpath
helm install airflow apache-airflow/airflow \
    --set webserver.defaultUser.password=RedHat123! \
    --set dags.gitSync.repo=https://github.com/redhat-na-ssa/mlops-prototype \
    --set dags.gitSync.branch=main \
    --set dags.gitSync.subPath=sepsis/airflow/workflows/dags

# Patch fixes postgresql pod creation
oc patch statefulset/airflow-postgresql --patch '{"spec":{"template":{"spec": {"serviceAccountName": "anyuid"}}}}'

# Error with replicaset-controller
'''
Error creating: pods "airflow-scheduler-5bfc85d854-" is forbidden: unable to validate against any security context constraint: [provider "anyuid": Forbidden: not usable by user or serviceaccount, provider restricted: .spec.securityContext.fsGroup: Invalid value: []int64{0}: 0 is not an allowed group, spec.initContainers[0].securityContext.runAsUser: Invalid value: 50000: must be in the ranges: [1000700000, 1000709999], spec.containers[0].securityContext.runAsUser: Invalid value: 50000: must be in the ranges: [1000700000, 1000709999], spec.containers[1].securityContext.runAsUser: Invalid value: 50000: must be in the ranges: [1000700000, 1000709999], provider "nonroot": Forbidden: not usable by user or serviceaccount, provider "hostmount-anyuid": Forbidden: not usable by user or serviceaccount, provider "machine-api-termination-handler": Forbidden: not usable by user or serviceaccount, provider "hostnetwork": Forbidden: not usable by user or serviceaccount, provider "hostaccess": Forbidden: not usable by user or serviceaccount, provider "node-exporter": Forbidden: not usable by user or serviceaccount, provider "privileged": Forbidden: not usable by user or serviceaccount]
Error creating: pods "airflow-statsd-7586f9998-" is forbidden: unable to validate against any security context constraint: [provider "anyuid": Forbidden: not usable by user or serviceaccount, spec.containers[0].securityContext.runAsUser: Invalid value: 65534: must be in the ranges: [1000700000, 1000709999], provider "nonroot": Forbidden: not usable by user or serviceaccount, provider "hostmount-anyuid": Forbidden: not usable by user or serviceaccount, provider "machine-api-termination-handler": Forbidden: not usable by user or serviceaccount, provider "hostnetwork": Forbidden: not usable by user or serviceaccount, provider "hostaccess": Forbidden: not usable by user or serviceaccount, provider "node-exporter": Forbidden: not usable by user or serviceaccount, provider "privileged": Forbidden: not usable by user or serviceaccount]
Error creating: pods "airflow-triggerer-b49cd5f8f-" is forbidden: unable to validate against any security context constraint: [provider "anyuid": Forbidden: not usable by user or serviceaccount, provider restricted: .spec.securityContext.fsGroup: Invalid value: []int64{0}: 0 is not an allowed group, spec.initContainers[0].securityContext.runAsUser: Invalid value: 50000: must be in the ranges: [1000700000, 1000709999], spec.containers[0].securityContext.runAsUser: Invalid value: 50000: must be in the ranges: [1000700000, 1000709999], provider "nonroot": Forbidden: not usable by user or serviceaccount, provider "hostmount-anyuid": Forbidden: not usable by user or serviceaccount, provider "machine-api-termination-handler": Forbidden: not usable by user or serviceaccount, provider "hostnetwork": Forbidden: not usable by user or serviceaccount, provider "hostaccess": Forbidden: not usable by user or serviceaccount, provider "node-exporter": Forbidden: not usable by user or serviceaccount, provider "privileged": Forbidden: not usable by user or serviceaccount]
'''

# Update policy for anyuid
# https://examples.openshift.pub/deploy/scc-anyuid/ 
'oc adm policy add-scc-to-user -n airflow -z airflow-flower anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-scheduler anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-statsd anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-triggerer anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-webserver anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-worker anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-run-airflow-migrations anyuid'
'oc adm policy add-scc-to-user -n airflow -z airflow-postresql anyuid'
oc adm policy add-scc-to-user -n airflow -z airflow-anyuid anyuid


## Manually scale the pods
oc scale deployment/airflow-flower --replicas=0
oc scale deployment/airflow-flower --replicas=1
oc scale deployment/airflow-scheduler --replicas=0
oc scale deployment/airflow-scheduler --replicas=1
oc scale deployment/airflow-statsd --replicas=0
oc scale deployment/airflow-statsd --replicas=1
oc scale deployment/airflow-triggerer --replicas=0
oc scale deployment/airflow-triggerer --replicas=1
oc scale deployment/airflow-webserver --replicas=0
oc scale deployment/airflow-webserver --replicas=1

# Port-forward for Airflow webserver
'oc port-forward svc/airflow-webserver 8080:8080'

# Permanently expose routes
oc expose svc/airflow-webserver
oc patch route/airflow-webserver --patch '{"spec":{"tls": {"termination": "edge", "insecureEdgeTerminationPolicy": "Redirect"}}}'