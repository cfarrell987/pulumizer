from aws import aws_dump  # pylint: disable=import-error
from tools import json,logger  # pylint: disable=import-error
if __name__ == "__main__":
    # TODO: Add support for multiple regions
    dump = aws_dump.get_resources("ca-central-1", "default")
    output = json.json_write(dump, 'resources.json')
    logger = logger.get_logger("apc.log")
