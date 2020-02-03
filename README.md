Welcome to OCTO Fly's documentation!
====================================

OCTO Fly project created for the AI certification.

Project Organization
------------

    ├── LICENSE
    ├── Makefile                        <- Makefile with useful commands
    ├── README.md                       <- The top-level README for developers using this project
    ├── config.py                       <- The top-level config file for this project
    │
    ├── data
    │   ├── external                    <- Data from third party sources
    │   ├── interim                     <- Intermediate data that has been transformed
    │   ├── processed                   <- Final outputs of the worflows
    │   └── raw                         <- The original, immutable data dump
    │
    │
    ├── deploy
    │   └── pipeline.yml                <- CI/CD pipeline
    │   
    │
    ├── docker
    │   ├── Dockerfile                  <- Simple DockerFile for the app
    │   ├── docker-compose-dev.yml      <- Used to launch your services locally / in dev
    │   └── docker-compose-prod.yml     <- Used to lauch your services in production
    │
    ├── docs                            <- Project documentation generated by Sphinx
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
    ├── flight_pred                     <- Modules for use in this project
    │   ├── __init__.py                 <- Makes flight_pred a Python module
    │   └── example.py
    │
    └── tests                           <- Unit and integrations tests
        └── test_example.py


--------

<p><small>*You can give a look at <a target="_blank" href="https://docs.prefect.io/">Prefect</a>.</small><p>

<p>Project based on the <a target="_blank" href="https://github.com/Caffeinside/cookiecutter-data-science-indus">cookiecutter data science industrialization project template</a>.</p>
