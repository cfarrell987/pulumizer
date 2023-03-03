# Pulumizer

Pulumizer or APC(AWS Pulumi Converter) is a tool used to create a json dump of all aws resources in a specified region

## Requirements
[Pulumi](https://www.pulumi.com/docs/get-started/aws/begin/)
[Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Usage
First, you will need to ensure you have configured your aws credentials in `~/.aws/credentials`
You can also specify a profile by adding it to the `.env` as `PROFILE='$PROFILE'`
Next, specify the region by adding it in the `.env` as `REGION='$REGION'`