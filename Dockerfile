# syntax=docker/dockerfile:1
FROM python:latest
RUN apt update && apt install python3-dev gcc -y curl
RUN useradd --create-home appuser
WORKDIR /app
USER appuser
RUN mkdir -p /home/appuser/.local/share/pypoetry
RUN curl -sSL https://install.python-poetry.org | python3 - --preview
ENV PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /home/appuser
COPY --chown=appuser:appuser pyproject.toml webhookfromghost.ini webhookfromghost.py poetry.lock wsgi.py requirements.txt entrypoint.sh /home/appuser/
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi
EXPOSE 5000/tcp
RUN chmod +x /home/appuser/entrypoint.sh
ENTRYPOINT ["/home/appuser/entrypoint.sh"]
