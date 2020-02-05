from setuptools import find_packages, setup

setup(
    name='octo_fly',
    author='BASA',
    author_email='basa@octo.com',
    version='0.1.0',
    description='OCTO Fly project created for the AI certification',
    packages=find_packages(),
    python_requires='~=3.7',
    install_requires=['pandas==0.25.3',
                      'numpy==1.18.1',
                      'prefect==0.9.1',
                      'streamlit==0.54.0',
                      'scikit-learn==0.19.2',
                      'scipy==1.4.1',
                      'pyarrow==0.12.1'],
    extras_require={'tests': ['pytest']}
)
