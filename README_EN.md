# Motion detection and notification App with Soracom Cloud Camera Service

This is an application that acquires motion detection events from the Soracom Cloud Camera Service via the SORACOM API and notifies LINE Notify with the images. You can deploy it using the AWS Serverless Application Model (SAM) template.

## Caution

The scripts in this repository are examples only and are not guaranteed to work. The content of this script is not intended for commercial use. Use at your own risk.

## Configuration

**Note that this script runs every minute by default.** 

1. Call AWS Lambda periodically with Amazon EventBridge
2. Retrieve a list of events in the past minute using the SORACOM API
3. Download images at the time the event occurred
Notify LINE Notify of downloaded images

(If there are multiple events, 3 and 4 are performed for all events.)

## Usage Procedure

Follow the steps below to use this service.

### Preparation

Prepare your account and environment. 

1. Prepare a camera that supports [Soracom Cloud Camera Service](https://soracom.jp/sora_cam/). (A license agreement is also required to use the API.)
2. Set up [LINE Notify](https://notify-bot.line.me/ja/)
3. Prepare an [AWS](https://aws.amazon.com/jp/?nc2=h_lg) account.
4. Prepare authentication information (authentication key ID, authentication key) for [SORACOM SAM User](https://users.soracom.io/ja-jp/docs/sam/)
5. Set up [AWS Serverless Application Model](https://aws.amazon.com/jp/serverless/sam/) (SAM)

### How to deploy the application

1. Prepare necessary environment variables for deploying `sora-cam-event-notification`.
   - soracomAuthKeyId: Authentication key ID for SORACOM SAM user
   - soracomAuthKey: Authentication key for SORACOM SAM user
   - deviceId: Device ID of the Soracom Cloud Camera Service enabled camera
   - lineNotifyToken: Token for LINE Notify
2. Build and deploy `sora-cam-event-notification`.
   - Use `sam build` and `sam deploy --guided`.

### Delete the application

Applications deployed with SAM can be removed from CloudFormation.
