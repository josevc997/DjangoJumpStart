FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1

USER vscode
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/home/vscode/.poetry/bin:$PATH"
RUN /home/vscode/.local/bin/poetry config virtualenvs.in-project true