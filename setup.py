import os
from setuptools import setup, find_packages

cd = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(cd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='thc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests[socks]'
    ],
    author='Wendel Frota',
    author_email='wendelalves898@gmail.com',
    description='HTTP Client for making requests through the Tor network',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wendelfrota/tor-http-client',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'thc=cli:main',
        ],
    },
)
