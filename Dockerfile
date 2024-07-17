FROM python:3.11

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /ssl

WORKDIR /app
ADD certificates /app/certificates
ADD signing /app/signing
ADD smokca /app/smokca
ADD manage.py /app/manage.py
ADD tests /app/tests
ADD __init__.py /app/__init__.py

RUN python manage.py collectstatic

VOLUME /db

CMD ["waitress-serve", "--listen=0.0.0.0:80", "--threads=4", "smokca.wsgi:application"]
