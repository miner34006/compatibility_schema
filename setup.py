from setuptools import find_packages, setup

setup(
    name='compatibility_schema_42',
    description='Compatibility schema for migration from 0.6.9 to 1+ versions',
    version='1.0.0',
    url='https://github.com/nikitanovosibirsk/district42',
    author='Polianok Bogdan',
    author_email='bogdan.polianok@gmail.com',
    python_requires='>=3.6',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Delorean==0.5.0',
        'valera==1.5.0',
        'revolt==1.5.1',
        'blahblah==1.5.0'
    ]
)
