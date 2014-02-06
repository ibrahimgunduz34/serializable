import os

from setuptools import setup, find_packages

package_idr = os.path.normpath(
    os.path.join(os.path.abspath(__file__), os.pardir))

setup(
    name='serializable',
    packages=find_packages(package_idr),
    version="1.1.3",
    author="ibrahimgunduz34",
    author_email="ibrahimgunduz34@gmail.com")
