# Configuration for Cluster

1. Htpasswd and OAuth for Authentication
    - https://www.redhat.com/sysadmin/openshift-htpasswd-oauth
1. Create a project "Sepsis Detection"
1. Add team to new project 
    - https://www.redhat.com/sysadmin/openshift-htpasswd-oauth
1. Installed Open Data Hub Operator
1. Applied kfdef from https://github.com/opendatahub-io/odh-manifests/blob/master/kfdef/kfctl_openshift.yaml following errors on default kfdef deployment
1. 
```
#Install ODH from CLI
$ oc get packagemanifests -n openshift-marketplace | grep opendatahub
```   