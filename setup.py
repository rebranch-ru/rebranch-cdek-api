from os.path import join, dirname

from setuptools import setup


setup(
    name='rebranch-cdek-api',
    version=0.1,
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Rebranch',
    package_data={},
    install_requires=[u'requests', ],
    url='https://github.com/rebranch/rebranch-cdek-api.git'
)