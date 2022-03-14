from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

setup(
    name="PatientKFold",
    version="0.0.1",
    description="A simple K-Fold cross-validator with 'group' awareness.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Danilo Weber Nunes",
    author_email="danilownunes@gmail.com",
    url="https://github.com/danilown/PatientKFold",
    license="MIT",
    install_requires=requirements,
    packages=find_packages(),
)
