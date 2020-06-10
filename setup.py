"""Setup file for reasoner package."""
from setuptools import setup

setup(
    name='reasoner_pydantic',
    version='0.1.0-dev',
    author='Patrick Wang',
    author_email='patrick@covar.com',
    url='https://github.com/ranking-agent/reasoner-pydantic',
    description='Pydantic models for the Reasoner API data formats',
    packages=['reasoner_pydantic'],
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    python_requires='>=3.6',
)
