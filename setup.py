import sys
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


version = sys.version_info[:2]
if version < (3, 8):
    print(
        "resources requires Python version 3.8 or later"
        + f" (you are using Python {version[0]}.{version[1]})."
    )
    sys.exit(-1)


VERSION = "0.1.0"

install_requires = ["boto3", "json", "pulumi"]

setup(
    name="Pulumizer",
    version=VERSION,
    description="A Script to pull all resources in an AWS Account and convert to a Pulumi Bulk Import JSON",
    long_description=long_description,
    author="Caleb Farrell",
    author_email="caleb.farrell@valhallahosting.com",
    url="https://github.com/cfarrell987/pulumizer",
    license="GPLv3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
