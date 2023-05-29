from setuptools import find_packages, setup

requirements = [
    'func_call_patcher',
    'django',
    'djangorestframework',
    'attrs',
]

setup(
    name='func_call_patcher_api',
    version='0.0.0',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)
