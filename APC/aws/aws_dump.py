import csv
import boto3
from tools import logger  # pylint: disable=import-error


logger = logger.get_logger("apc.log")

"""
Using the supported_services.csv file get all services
that are supported by ResourceGroupsTaggingAPI
"""


def get_services():
    # TODO: Move file to a CDN and pull on first run, verify checksum and update if needed
    with open("./resources/supported_services.csv", "r", encoding="UTF8") as file:
        reader = csv.reader(file)
        supported_services = [row[0] for row in reader][1:]

    return supported_services


# TODO: Add support for multiple profiles
def boto3_init(region, profile):
    boto3.setup_default_session(profile_name=profile)
    services = get_services()
    client = boto3.client("resourcegroupstaggingapi", region_name=region)
    paginator = client.get_paginator("get_resources")

    return services, paginator


# Using ResourceGroupsTaggingAPI get all resources within a specific region
def get_resources(services, paginator):
    resources = {"resources": []}

    for service in services:
        for response in paginator.paginate(ResourceTypeFilters=[service]):
            """
            Check if the pagination token is empty,
            if it is then break the loop as this service is empty
            """
            if response["PaginationToken"] == "":
                logger.error("Pagination token is empty for: " + service)
                break

            for resource in response["ResourceTagMappingList"]:
                arn = resource["ResourceARN"]
                arn_block = arn.split(":")
                main_service = arn_block[2]
                service = arn_block[5].split("/")[0]
                resource_type = (
                    f"aws:{main_service.lower()}/{service}:{service.capitalize()}"
                )
                resource_id = resource["ResourceARN"].split(":")[-1].split("/")[1]
                tags = {tag["Key"]: tag["Value"] for tag in resource["Tags"]}
                name = tags.get("Name", resource_id)

                if name != "":
                    logger.info("No name tag found for resource: " + resource_id)

                else:
                    logger.info("Name tag found for resource: " + resource_id)
                    name = resource["ResourceARN"].split(":")[-1].split("/")[-1]

                if main_service not in resources:
                    resources[main_service] = []
                resources.setdefault("resources", []).append(
                    {
                        "Type": resource_type,
                        "name": name,
                        "id": resource_id,
                        "ARN": arn,
                        "tags": tags,
                    }
                )

    return resources
