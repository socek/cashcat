"""
About this project

"""

from setuptools import find_packages
from setuptools import setup

setup(
    name='cashcat',
    version='0.1',
    description='',
    packages=find_packages(),
    install_requires=[],
    tests_require=['coverage', 'freezegun', 'pytest', 'pytest-cov', 'WebTest'],
    long_description=__doc__,
    author='Dominik "Socek" Długajczyk',
    author_email='msocek@gmail.com',
    license='MIT',
    zip_safe=False,
    url='http://github.com/socek/cashcat',
    entry_points={
        'paste.app_factory': ['main = cashcat.application.startpoints:uwsgi'],
    },
    classifiers=[
        'Development Status :: 4 - Beta', 'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
)
