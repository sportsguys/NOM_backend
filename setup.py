from setuptools import find_packages, setup

setup(
    name='server',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask==1.1.2',
        'sqlalchemy==1.4.8',
        'Click==7.1.2',
        'pymysql==1.0.2',
        'numpy==1.19.4',
        'html5lib==1.1',
        'requests==2.25.1',
        'bs4'
    ]
)