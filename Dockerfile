
FROM python:3.12-slim


WORKDIR /app


COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev --no-root


COPY . /app/


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
