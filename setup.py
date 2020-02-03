from setuptools import find_packages, setup

setup(
    name='octo_fly',
    author='BASA',
    author_email='basa@octo.com',
    version='0.1.0',
    description='OCTO Fly project created for the AI certification',
    packages=find_packages(),
    python_requires='~=3.7',
    install_requires=['pandas',
                      'numpy',
                      'prefect',
                      'streamlit',
                      'sklearn'],
    extras_require={'tests': ['pytest']}
)
