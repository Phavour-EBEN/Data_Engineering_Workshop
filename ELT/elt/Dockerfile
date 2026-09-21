FROM python:3.13-slim

RUN apt-get update && apt-get install -y postgresql-client cron

COPY start.sh/app/start.sh

COPY elt_script.py .

CMD [ "python", "elt_script.py" ]