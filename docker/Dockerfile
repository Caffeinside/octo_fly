FROM continuumio/miniconda3:latest
SHELL ["/bin/bash", "-c"]

EXPOSE 8501

RUN apt-get update -y
RUN apt-get install -y build-essential
RUN mkdir /app

COPY setup.py /app/setup.py
COPY Makefile /app/Makefile
COPY src /app/src

WORKDIR /app

RUN make create_environment
RUN source activate octo_fly
RUN pip install -e .

CMD streamlit run src/example.py