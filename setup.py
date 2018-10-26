"""
Setup for Unit XBlock
"""

import os
from setuptools import setup


def package_data(pkg, roots):
    """
    Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.
    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}

def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip() for line in open(path).readlines()
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return not (
        line == '' or
        line.startswith('-r') or
        line.startswith('#') or
        line.startswith('-e') or
        line.startswith('git+')
    )

setup(
    name='unit-xblock',
    version='0.1',
    description='XBlock for grouping other XBlocks together into a "unit" of learning',
    license='AGPL v3',
    packages=[
        'unit_xblock',
    ],
    install_requires=load_requirements('requirements/base.in'),
    entry_points={
        'xblock.v1': [
            'unit = unit_xblock:UnitXBlock',
        ]
    },
    package_data=package_data("unit_xblock", []),
)
