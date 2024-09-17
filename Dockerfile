FROM tiangolo/uvicorn-gunicorn:python3.11

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

RUN pip install --no-cache-dir --no-deps -e .
