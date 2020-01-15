from setuptools import setup, find_packages
import simplesql

setup(
name='simplesql',
    version=simplesql.__version__,
    packages=find_packages(),
    author="Thomas Be:.",
    author_email="",
    description="SimpleSQL Connections & Database Management",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/Thomas-SBE/pythonsqlconnector',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: Release & In Developement",
        "Natural Language :: French & English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database Management",
    ],
    entry_points = {
        'console_scripts': [],
    },
    license="OpenSource",
)