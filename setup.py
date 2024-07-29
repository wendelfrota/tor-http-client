from setuptools import setup

setup(
    name='tor_http_client',
    version='0.1.0',
    py_modules=['tor_http_client'],
    install_requires=[
        'requests',
    ],
    author='Wendel Frota',
    author_email='wendelalves898@gmail.com',
    description='HTTP Client for making requests through the Tor network',
    url='https://github.com/wendelfrota/tor-http-client',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
