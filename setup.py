from setuptools import find_packages, setup


requirements = [r for r in open('requirements.txt', 'r').read().splitlines()]

setup(
    name='radiologi',
    version='0.0.1',
    license='BSD',
    description='Modul Farmasi.',
    long_description_content_type='text/markdown',
    author='Andika Fransisko',
    packages=find_packages(include=['radiologi']),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10.6",
    zip_safe=False
)