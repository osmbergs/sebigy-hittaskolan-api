#
FROM python:3.12


COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


COPY root.crt /root/.postgresql/root.crt
COPY start.sh start.sh
COPY app app
COPY alembic alembic

COPY alembic.ini alembic.ini

RUN chmod +x start.sh

CMD ["./start.sh"]