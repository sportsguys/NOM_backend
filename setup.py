from setuptools import find_packages, setup

setup(
    name='server',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy==1.4.8',
        'Click',
        'pymysql',
        'numpy',
        'html5lib',
        'requests',
        'bs4'
    ],
    entry_points={
        "console_scripts": [
            "startserver=cli:start_server"
        ],
    }
)