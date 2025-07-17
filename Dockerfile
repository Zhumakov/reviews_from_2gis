FROM python:3.13


WORKDIR /project

RUN pip install uv
COPY pyproject.toml .
RUN uv pip install . --system
RUN playwright install-deps
RUN playwright install chromium

COPY . .
