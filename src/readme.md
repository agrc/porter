# conductor

a bot that checks on the existence of data and required fields

![conductor_sm](https://user-images.githubusercontent.com/325813/90076216-62563280-dcbc-11ea-8023-afa62e75b04b.png)

## prerequisites

1. enable

   - cloud pub sub subscription
     - `gcloud services enable pubsub.googleapis.com`
   - cloud run api\*
     - `gcloud services enable run.googleapis.com`
   - cloud container registry api\*
     - `gcloud services enable containerregistry.googleapis.com`
   - cloud scheduler api\*
     - `gcloud services enable cloudscheduler.googleapis.com`
   - cloud secrets api\*
     - `gcloud services enable secretmanager.googleapis.com`
   - cloud compute engine
     - `gcloud services enable compute.googleapis.com`

1. give google cloud default compute service account view access to stewardship spreadsheet
1. Request DTS to attach the project to the DTS [dev, prod] Shared VPC

_\* requires billing_

## cloud configuration

1. Update project id in `src/conductor/server.py:43`
1. Create a `client-secret.json` file with sheet privileges and read access to the stewardship spreadsheet.

### cloud registry

1. build image
   - `docker build . -t conductor`
1. tag image in GCR
   - `docker tag conductor gcr.io/ut-dts-agrc-porter-prod/conductor`
1. push image to GCR
   - `docker push gcr.io/ut-dts-agrc-porter-prod/conductor`

```bash
docker build . -t conductor &&
docker tag conductor gcr.io/ut-dts-agrc-porter-prod/conductor &&
docker push gcr.io/ut-dts-agrc-porter-prod/conductor
```

### cloud run

1. create a service named `conductor`
1. authentication: `require authentication`
1. choose latest container image
   - `gcr.io/ut-dts-agrc-porter-prod/conductor@latest`
1. Request timeout: `300`
1. Maximun intances: `10`
1. enable shared VPC connector
   - `gcloud run services update conductor --vpc-connector projects/ut-dts-shared-vpc-dev/locations/us-central1/connectors/dts-shared-vpc-connector`
   - `gcloud alpha run services update conductor --vpc-connector=projects/ut-dts-shared-vpc-dev/locations/us-central1/connectors/dts-shared-vpc-connector --vpc-egress=all --platform managed --zone us-central1`
1. copy cloud run url for the subscription

### subscriptions

1. create topic with id: `conductor-topic`
1. create subscription with id: `conductor-subscription` pointed at the newly created topic

   - delivery type: `push`
   - expiration: `never expires`
   - push endpoint: `<cloud run service url>/gcp/schedule`
   - acknowledgement deadline: `300 seconds`
   - message retention: `30 minutes`
   - retry policy: `min: 10; max: 60`

### scheduler

1. create job named `conductor`

   - frequency: `0 9 * * 1`
   - time zone: `America/Denver (MDT)`
   - target: `Pub/Sub`
   - topic: `conductor-topic`
   - payload: `{ "now": true }`

### secrets

1. create secret as valid json with name: `conductor-connections`
1. give default compute service account `secret manager secret accessor` role

## Development

1. use `test_conductor` as the entry point
1. set the `service_account_file` path to a service account file with access to the stewardship sheet
