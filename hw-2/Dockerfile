FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
COPY generate_example.py ./
COPY includes/ ./includes/

RUN mkdir -p artifacts

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

RUN python generate_example.py

RUN cd artifacts && pdflatex -interaction=nonstopmode task_2_2.tex
