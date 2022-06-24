# ODH Setup

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