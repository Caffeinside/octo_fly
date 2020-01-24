OCTO Fly
==============================

OCTO Fly project created for the AI certification

Project Organization
------------

    ├── LICENSE
    ├── Makefile                        <- Makefile with useful commands
    ├── README.md                       <- The top-level README for developers using this project
    ├── airflow                         <- Target folder to generate Airflow DAGs
    ├── config.py                       <- The top-level config file for this project
    │
    ├── data
    │   ├── external                    <- Data from third party sources
    │   ├── interim                     <- Intermediate data that has been transformed
    │   ├── processed                   <- Final outputs of the worflows
    │   ├── raw                         <- The original, immutable data dump
    │   └── reference                   <- Reference or mapping data
    │
    ├── deploy
    │   ├── azure-cd-pipeline.yml       <- CD pipeline to retrieve Docker images and deploy the app on a remote server
    │   └── azure-ci-pipeline.yml       <- CI pipeline to run tests, build and push Docker images to a registry
    │
    ├── docker
    │   ├── Dockerfile                  <- Simple DockerFile for the app
    │   ├── docker-compose-dev.yml      <- Used to launch your services locally / in dev
    │   └── docker-compose-prod.yml     <- Used to lauch your services in production
    │
    ├── docs                            <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                          <- Trained and serialized models
    │
    ├── notebooks                       <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                                      the creator's initials, and a short `-` delimited description, e.g.
    │                                      `1.0-jqp-initial-data-exploration`
    │
    ├── pipeline
    │   ├── predict.py                  <- ML prediction worflow*
    │   └── train.py                    <- ML training worflow*
    │
    ├── scripts                         <- Stand-alone scripts to perform specific tasks
    │
    ├── setup.py                        <- Makes project pip installable (pip install -e .) so src can be imported and 
    │                                      dependencies installed
    │
    ├── src                             <- Source code for use in this project
    │   ├── __init__.py                 <- Makes src a Python module
    │   └── example.py
    │
    └── tests                           <- Unit and integrations tests
        └── test_example.py


--------

<p><small>*You can give a look at <a target="_blank" href="https://github.com/octo-technology/ddapi">Data Driver</a>.</small><p>

<p>Project based on the <a target="_blank" href="https://github.com/Caffeinside/cookiecutter-data-science-indus">cookiecutter data science industrialization project template</a>.</p>
