# Conductor

## Prerequisites

1. enable
   - cloud pub sub subscription
   - cloud run api\*
   - cloud container registry api\*
   - cloud scheduler api\*
   - cloud secrets api\*

_\* requires billing_

1. accept pub/sub topics

   - add flask to the project
     - `pip install flask gunicorn`

1. access cloud secrets

   - `pip install google-cloud-secret-manager`
   - give default compute service account secret accessor role

1. create secret as valid json

1. create cloud run service

1. give cloud default compute service account access to stewardship spreadsheet

1. create a pub sub topic and subscription

   - subscription should push to the cloud run url

1. create a cron job to publish the topic

## Deploy

```bash
docker build . -t conductor &&
docker tag conductor gcr.io/ut-dts-agrc-porter-prod/conductor &&
docker push gcr.io/ut-dts-agrc-porter-prod/conductor
```
