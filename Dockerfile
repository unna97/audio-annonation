FROM continuumio/miniconda3:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /audio-annonation

COPY environment.yml .

RUN conda env create -n comedy-project-docker -f environment.yml && \
    conda clean -afy

SHELL ["conda", "run", "-n", "comedy-project-docker", "/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["conda", "run", "--no-capture-output", "-n", "comedy-project-docker", "gunicorn", "--bind", "0.0.0.0:8000", "audio-annonation.wsgi:application"]