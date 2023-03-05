import csv
import boto3
from tools import logger  # pylint: disable=import-error


logger = logger.get_logger("apc.log")


# Using the ServiceQuotas API get all services within a specific region
def get_services():
    # TODO: Move file to a CDN and pull on first run, verify checksum and update if needed
    with open("./resources/supported_services.csv", "r", encoding="UTF8") as file:
        reader = csv.reader(file)
        supported_services = [row[0] for row in reader][1:]

    return supported_services


# Using ResourceGroupsTaggingAPI get all resources within a specific region
def get_resources(region, profile):
    # TODO: Add support for multiple profiles
    boto3.setup_default_session(profile_name=profile)
    services = get_services()
    print(services)
    client = boto3.client("resourcegroupstaggingapi", region_name=region)

    paginator = client.get_paginator("get_resources")
    resources = {"resources": []}

    for service in services:
        paginator = client.get_paginator("get_resources")
        for response in paginator.paginate(ResourceTypeFilters=[service]):
            if response["PaginationToken"] == "":
                logger.error("Pagination token is empty for: " + service)
                break

            for resource in response["ResourceTagMappingList"]:
                main_service = resource["ResourceARN"].split(":")[2]
                arn = resource["ResourceARN"]
                resource_service = resource["ResourceARN"].split(":")[5].split("/")[0]
                resource_id = resource["ResourceARN"].split(":")[-1]
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
                        "Type": resource_service,
                        "name": name,
                        "id": resource_id,
                        "ARN": arn,
                        "tags": tags,
                    }
                )

    return resources
