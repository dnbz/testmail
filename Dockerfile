FROM python:3.11-slim
WORKDIR /app

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm==2.8.2

COPY pyproject.toml pdm.lock ./
RUN pdm install --prod --no-lock --no-editable

COPY . .

CMD ["pdm", "run", "serve-prod"]
