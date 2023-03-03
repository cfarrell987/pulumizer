import json
import csv
import boto3


# Using the ServiceQuotas API get all services within a specific region
def get_services():

    # TODO: Move file to a CDN and pull on first run, verify checksum and update if needed
    with open("./resources/supported_services.csv", "r", encoding='UTF8') as file:
        reader = csv.reader(file)
        supported_services = [row[0] for row in reader][1:]

    return supported_services


# Using ResourceGroupsTaggingAPI get all resources within a specific region
def get_resources(region):

    # TODO: Add support for multiple profiles
    boto3.setup_default_session(profile_name="default")
    services = get_services()
    print(services)
    client = boto3.client("resourcegroupstaggingapi", region_name=region)

    paginator = client.get_paginator("get_resources")
    resources = {}

    for service in services:
        print(service)
        paginator = client.get_paginator("get_resources")
        for response in paginator.paginate(ResourceTypeFilters=[service]):
            for resource in response["ResourceTagMappingList"]:
                main_service = resource["ResourceARN"].split(":")[2]
                arn = resource["ResourceARN"]
                resource_service = resource["ResourceARN"].split(":")[5].split("/")[0]
                name = resource["ResourceARN"].split("/")[-1]
                # tags = [{'Key': k, 'Value': v} for k, v in resource['Tags'].items()]
                if main_service not in resources:
                    resources[main_service] = []
                resources.setdefault(resource_service, []).append(
                    {
                        "Type": resource_service,
                        "Name": name,
                        "ARN": arn,
                    }
                )
                print(resource)

    for resource in resources:
        print(resource)

    with open("resources.json", "w", encoding='UTF8') as file:
        json.dump(resources, file, indent=4)

    return resources
