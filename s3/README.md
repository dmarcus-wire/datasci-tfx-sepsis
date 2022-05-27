# Configuring S3 Bucket for OpenShift usage

1. Administrator Creates Secret via aws-s3-secret.yaml
2. Administrator Creates StorageClass via the {greenfield or brownfield}-storageclass.yaml
3. 

## Administrator Creates Secret with the aws-s3-creds.yaml

you need to set four values
1. Name of the secret, this will be referenced in StorageClass.
2. Namespace where the Secret will exist.
3. Your AWSACCESSKEY_ID base64 encoded.
4. Your AWSSECRETACCESS_KEY base64 encoded.

you need to apply the file
`# kubectl create -f aws-s3-creds.yaml`

## Administrator Creates StorageClass with the {greenfield or brownfield}-storageclass.yaml

you need to set six values 
1. Name of the StorageClass, this will be referenced in the User ObjectBucketClaim.*
2. Provisioner name*
3. AWS Region that the StorageClass will serve*
4. Name of the bucket owner Secret created above*
5. Namespace where the Secret will exist*
6. reclaimPolicy (Delete or Retain) indicates if the bucket can be deleted when the OBC is deleted. NOTE: the absence of the bucketName Parameter key in the storage class indicates this is a new bucket and its name is based on the bucket name fields in the OBC.

*apply only for brownfield

you need to apply the file
`# kubectl create -f storageclass-brownfield.yaml`

## User Creates ObjectBucketClaim with the {greenfield or brownfield}-objectbucketclaim.yaml

you need to set five values
1. Name of the OBC*
2. Namespace of the OBC*
3. Name prepended to a random string used to generate a bucket name. It is ignored if bucketName is defined
4. Name of new bucket which must be unique across all AWS regions, otherwise an error occurs when creating the bucket. If present, this name overrides generateName
5. StorageClass name* 

NOTE: if both generateBucketName and bucketName are omitted, and the storage class does not define a bucket name, then a new, random bucket name is generated with no prefix.

*apply only for brownfield

you need to apply the file
`# kubectl create -f obc-brownfield.yaml`

## User Creates / Update Pod

you need to update the Pod spec values
1. Name of the generated configmap from the provisioning process
2. Name of the generated secret from the provisioning process 
NOTE: Generated ConfigMap and Secret are same name as the OBC!


```
spec:
  containers:
  ....
    envFrom:
    - configMapRef:
        name: my-awesome-bucket <1>
    - secretRef:
        name: my-awesome-bucket <2>
```