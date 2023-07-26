"""Setup file for reasoner package."""
from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="reasoner-pydantic",
    version="4.1.2",
    author="Abrar Mesbah",
    author_email="amesbah@covar.com",
    url="https://github.com/TranslatorSRI/reasoner-pydantic",
    description="Pydantic models for the Reasoner API data formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["reasoner_pydantic"],
    include_package_data=True,
    install_requires=["pydantic>=1.8"],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.6",
)
