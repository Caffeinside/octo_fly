from setuptools import find_packages, setup

setup(
    name='OCTO Fly',
    author='BASA',
    description='OCTO Fly project created for the AI certification',
    packages=find_packages(),
    setup_requires=['setuptools_scm'],
    python_requires='~=3.7',
    install_requires=['python-dotenv', 'pandas', 'numpy'],
    extras_require={'tests': ['pytest']},
    version='0.1.0'
)
