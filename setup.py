from setuptools import find_packages, setup

deps = {'tests': ['flake8']}

setup(
    name='template-project',
    version='0.0.1',
    description='Template Project',
    install_requires=[r.strip() for r in open('requirements.txt').readlines()],
    extras_require=deps,
    tests_require=deps['tests'],
    setup_requires=deps['tests'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    entry_points={'console_scripts': ['template-cli = template_project.cli:cli']},
)
