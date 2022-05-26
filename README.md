# Machine Learning Operations Prototype

Goal: Goal:  Demonstrate MLOps Lifecycle automation using the scenario of predicting patient at-risk of sepsis based on patient data

“MLOps is a practice for collaboration and communication between data scientists and operations professionals to help manage production ML lifecycle.”

“Similar to the DevOps or DataOps approaches, MLOps looks to increase automation and improve the quality of production ML while also focusing on business and regulatory requirements.”

![MLOps Demo Flow](./tfx-pipeline-on-openshift.png)


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


Resources
- https://www.iteblog.com/ppt/dataai-summit-europe-2020/streaming-inference-with-apache-beam-and-tfx-iteblog.com.pdf
