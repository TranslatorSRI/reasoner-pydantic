"""Setup file for reasoner package."""
from setuptools import setup

setup(
    name="reasoner-pydantic",
    version="2.2.3",
    author="Kenneth Morton",
    author_email="kenny@covar.com",
    url="https://github.com/TranslatorSRI/reasoner-pydantic",
    description="Pydantic models for the Reasoner API data formats",
    packages=["reasoner_pydantic"],
    include_package_data=True,
    install_requires=["pydantic>=1.8"],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.6",
)
