FROM jupyter/base-notebook

WORKDIR /home/jovyan

USER root
RUN pip install poetry
USER jovyan

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . ./

USER root
RUN apt-get update && apt-get install -y graphviz
USER jovyan

