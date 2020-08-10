# conductor

## prerequisites

1. enable

   - cloud pub sub subscription
   - cloud run api\*
   - cloud container registry api\*
   - cloud scheduler api\*
   - cloud secrets api\*

1. give google cloud default compute service account view access to stewardship spreadsheet

_\* requires billing_

## cloud configuration

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
1. enable shared VPC connector
   - `gcloud run services update conductor --vpc-connector projects/ut-dts-shared-vpc-dev/locations/us-central1/connectors/dts-shared-vpc-connector`

### subscriptions

1. create topic with id: `conductor`
1. create subscription with id: `conductor` pointed at the newly created topic

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
   - topic: `conductor`
   - payload: `{ "now": true }`

### secrets

1. create secret as valid json with name: `conductor-connections`
1. give default compute service account secret accessor role
