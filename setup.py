from setuptools import setup, find_packages

setup(
    name='joesTime',
    version='0.10',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'pytz',
        'typing',
        'datetime',
        'ipython',
        'black',
        'pytest'
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='tests',
)