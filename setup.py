from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "setuptools",
        "parakimo",
        "scp",
        "python-dotenv",
        "matplotlib",
        "python-dateutil"
    ],
    entry_points={
        'console_scripts': [
            'Tool-Data=my_module.main:main',  # Adjust this to your entry point
        ],
    },
)
