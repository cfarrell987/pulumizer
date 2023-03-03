import boto3 as boto
import pulumi
from aws import aws_dump

if __name__ == "__main__":
    # TODO: Add support for multiple regions
    dump = aws_dump.get_resources("ca-central-1")
