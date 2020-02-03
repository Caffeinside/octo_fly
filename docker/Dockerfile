FROM continuumio/miniconda3:4.7.12
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install gcc -y

RUN mkdir octo_fly

EXPOSE 8501

COPY . octo_fly

WORKDIR octo_fly

ENV PYTHONPATH "${PYTHON_PATH}:/octo_fly"

RUN conda create --name octo_fly python==3.7
RUN source activate octo_fly
RUN pip install .
