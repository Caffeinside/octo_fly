FROM continuumio/miniconda3:latest
SHELL ["/bin/bash", "-c"]

RUN mkdir /octo_fly

EXPOSE 8501

COPY . /octo_fly

WORKDIR /octo_fly

RUN conda create --name octo_fly python==3.7
RUN conda activate octo_fly
RUN pip install .

CMD streamlit run app/display_predictions.py
