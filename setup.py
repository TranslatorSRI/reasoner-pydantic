"""Setup file for reasoner package."""
from setuptools import setup

setup(
    name="reasoner-pydantic",
    version="1.1.1",
    author="Patrick Wang",
    author_email="patrick@covar.com",
    url="https://github.com/TranslatorSRI/reasoner-pydantic",
    description="Pydantic models for the Reasoner API data formats",
    packages=["reasoner_pydantic"],
    include_package_data=True,
    install_requires=[
        "pydantic>=1.5"
    ],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.6",
)
