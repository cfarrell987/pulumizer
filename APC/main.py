from aws import aws_dump  # pylint: disable=import-error
from tools import json, logger  # pylint: disable=import-error

if __name__ == "__main__":
    # TODO: Add support for multiple regions
    services, paginator = aws_dump.boto3_init("ca-central-1", "passiv")
    dump = aws_dump.get_resources(services, paginator)
    output = json.json_write(dump, "resources.json")
    logger = logger.get_logger("apc.log")
