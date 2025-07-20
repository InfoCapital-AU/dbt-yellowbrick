#!/usr/bin/env python
import os
import sys
import re
from pathlib import Path

if sys.version_info < (3, 8):
    print("Error: dbt does not support this version of Python.")
    print("Please upgrade to Python 3.8 or higher.")
    sys.exit(1)


from setuptools import setup

try:
    from setuptools import find_namespace_packages
except ImportError:
    # the user has a downlevel version of setuptools.
    print("Error: dbt requires setuptools v40.1.0 or higher.")
    print('Please upgrade setuptools with "pip install --upgrade setuptools" ' "and try again")
    sys.exit(1)

PSYCOPG2_MESSAGE = """
No package name override was  set.
Using 'psycopg2-binary' package to satisfy 'psycopg2'

If you experience segmentation faults, silent crashes, or installation errors,
consider retrying with the 'DBT_PSYCOPG2_NAME' environment variable set to
'psycopg2'. It may require a compiler toolchain and development libraries!
""".strip()

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()


def _dbt_psycopg2_name():
    # if the user chose something, use that
    package_name = os.getenv("DBT_PSYCOPG2_NAME", "")
    if package_name:
        return package_name

    # default to psycopg2-binary for all OSes/versions
    print(PSYCOPG2_MESSAGE)
    return "psycopg2-binary"


def _get_plugin_version_dict():
    _version_path = os.path.join(this_directory, "dbt", "adapters", "yellowbrick", "__version__.py")
    _semver = r"""(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"""
    _pre = r"""((?P<prekind>a|b|rc)(?P<pre>\d+))?"""
    _version_pattern = fr"""version\s*=\s*["']{_semver}{_pre}["']"""
    with open(_version_path) as f:
        match = re.search(_version_pattern, f.read().strip())
        if match is None:
            raise ValueError(f"invalid version at {_version_path}")
        return match.groupdict()



# used for this adapter's version
VERSION = Path(__file__).parent / "dbt/adapters/yellowbrick/__version__.py"
dbt_core_version = "1.10.0"
package_version = "1.10.0"

def _plugin_version() -> str:
    """
    Pull the package version from the main package version file
    """
    attributes = {}
    exec(VERSION.read_text(), attributes)
    return attributes["version"]


package_name = "dbt-yellowbrick"
description = """The Yellowbrick Data adapter plugin for dbt (data build tool)"""

DBT_PSYCOPG2_NAME = _dbt_psycopg2_name()

setup(
    name=package_name,
    version=_plugin_version(),
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Antelmi",
    author_email="david.antelmi@infocapital.com.au",
    url="https://github.com/InfoCapital-AU/dbt-yellowbrick.git",
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    package_data={
        "dbt": [
            "include/yellowbrick/dbt_project.yml",
            "include/yellowbrick/sample_profiles.yml",
            "include/yellowbrick/macros/*.sql",
            "include/yellowbrick/macros/**/*.sql",
        ]
    },
    install_requires=[
        "psycopg2-binary>=2.9,<3.0",
        "dbt-adapters>=1.7.0,<2.0",
        # add dbt-core to ensure backwards compatibility of installation, this is not a functional dependency
        "dbt-core>=1.9.0,<2.0",
        # installed via dbt-adapters but used directly
        "dbt-common>=1.0.4,<2.0",
        "agate>=1.0,<2.0"
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires=">=3.8",
)
