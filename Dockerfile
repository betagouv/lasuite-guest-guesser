FROM python:3.12.3-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY config.py /code/config.py
RUN mkdir -p data
RUN rm -rf data/*.csv
RUN apt-get update && apt-get install -y wget
RUN wget -O data/liste-administrations.csv https://www.data.gouv.fr/fr/datasets/r/c0f355f1-66bd-4f57-8a3c-2c6f3527b364
CMD ["fastapi", "run", "app/api.py", "--port", "80"]