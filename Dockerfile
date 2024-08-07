FROM continuumio/miniconda3:latest AS base

LABEL maintainer=Unnati

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


# Entrypoint stage (for ensuring db exists)
COPY db-entrypoint.sh ./db-entrypoint.sh
COPY web-entrypoint.sh ./web-entrypoint.sh
RUN chmod +x ./db-entrypoint.sh ./web-entrypoint.sh
ENTRYPOINT ["./web-entrypoint.sh"]


# Migration stage:
FROM base AS migrate
COPY . .
# echo:
RUN echo "running migrations" && conda run -n comedy-project-docker python manage.py migrate && \
echo "migrations done, running collectstatic" && conda run -n comedy-project-docker python manage.py collectstatic --noinput



# Application stage:
FROM base AS app

COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["conda", "run", "--no-capture-output", "-n", "comedy-project-docker", "gunicorn", "--bind", "0.0.0.0:8000", "audio-annonation.wsgi:application"]