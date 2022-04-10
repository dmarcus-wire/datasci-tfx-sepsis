# Follow Dwhite project
https://github.com/davwhite/airflow-helm

# Deploy Airflow on OpenShift
oc new-project airflow

# Change to project airflow
oc project airflow

# Install Helm Chart
helm repo add apache-airflow https://airflow.apache.org && helm repo update

# Update policy for anyuid
# https://examples.openshift.pub/deploy/scc-anyuid/ 
'''
oc adm policy add-scc-to-user -n airflow -z airflow-flower anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-scheduler anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-statsd anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-triggerer anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-webserver anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-worker anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-run-airflow-migrations anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-postresql anyuid &&
oc adm policy add-scc-to-user -n airflow -z airflow-anyuid anyuid
'''

## Manually scale the pods
'''
oc scale deployment/airflow-flower --replicas=0 && 
oc scale deployment/airflow-flower --replicas=1 &&
oc scale deployment/airflow-scheduler --replicas=0 &&
oc scale deployment/airflow-scheduler --replicas=1 &&
oc scale deployment/airflow-statsd --replicas=0 &&
oc scale deployment/airflow-statsd --replicas=1 &&
oc scale deployment/airflow-triggerer --replicas=0 &&
oc scale deployment/airflow-triggerer --replicas=1 &&
oc scale deployment/airflow-webserver --replicas=0 &&
oc scale deployment/airflow-webserver --replicas=1
'''

# Port-forward for Airflow webserver
'oc port-forward svc/airflow-webserver 8080:8080'

# Permanently expose routes
oc expose svc/airflow-webserver && oc patch route/airflow-webserver --patch '{"spec":{"tls": {"termination": "edge", "insecureEdgeTerminationPolicy": "Redirect"}}}'

# Errors
'''
Readiness probe failed: % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 0 0 0 0 0 0 0 0 --:--:-- --:--:-- --:--:-- 0curl: (7) Failed to connect to localhost port 5555: Connection refused

Error creating: pods "airflow-run-airflow-migrations--1-" is forbidden: unable to validate against any security context constraint: [provider "anyuid": Forbidden: not usable by user or serviceaccount, provider restricted: .spec.securityContext.fsGroup: Invalid value: []int64{1000770000}: 1000770000 is not an allowed group, spec.containers[0].securityContext.runAsUser: Invalid value: 1000770000: must be in the ranges: [1000660000, 1000669999], provider "nonroot": Forbidden: not usable by user or serviceaccount, provider "hostmount-anyuid": Forbidden: not usable by user or serviceaccount, provider "machine-api-termination-handler": Forbidden: not usable by user or serviceaccount, provider "hostnetwork": Forbidden: not usable by user or serviceaccount, provider "hostaccess": Forbidden: not usable by user or serviceaccount, provider "node-exporter": Forbidden: not usable by user or serviceaccount, provider "privileged": Forbidden: not usable by user or serviceaccount]
'''

# References
- https://dsri.maastrichtuniversity.nl/docs/workflows-airflow/
- https://github.com/MaastrichtU-IDS/dsri-documentation/blob/master/applications/airflow/values.yml