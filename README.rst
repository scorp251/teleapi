TeleAPI
=======
HTTP API for working with telegram messages
-------------------------------------------

** TeleAPI ** is python daemon based on flask. It serve HTTP requests for sending message to telegram

Features
--------
- REST API
- Can serve JSON
- Both cleartext and base64 encoded messages
- Web based contact list editor
- Recieves telegram messages and log it into file

Requirements
------------

-   Python 3.5 or higher.
-   A `Telegram API key <https://core.telegram.org/api/obtaining_api_id>`_


Installing
----------

.. code-block:: shell

    cd /opt
    git clone https://github.com/scorp251/teleapi
    cd teleapi
    virtualenv .venv
    .venv/bin/activate
    pip install -r requirements.txt

Getting Started
---------------

Copy file config.ini.sample to config.ini and fill requiered fields

First run:

.. code-block:: shell

    cd /opt/teleapi
    .venv/bin/flask run

In console it will ask you phone number and security code


For normal execution run from main directory

.. code:: shell

    ./run.sh

Configure NGINX

.. code-block:: shell

    server {
        listen 0.0.0.0:80;

        location / {
            proxy_pass              http://127.0.0.1:5000;
            proxy_read_timeout      30;
        }

        location /contacts/static {
            root /opt/teleapi/app;
       }
    }

Better run from supervisord

.. code-block:: ini

    [supervisorctl]

    [supervisord]
    logfile=/var/log/supervisord.log
    user=root

    [program:teleapi]
    directory=/opt/teleapi
    command=/opt/teleapi/.venv/bin/gunicorn -b 127.0.0.1:5000 app:app
    stdout_logfile=/var/log/supervisor-teleapi.log
    stderr_logfile=/var/log/supervisor-teleapi.log
    autorestart=true


Usage
---------------
To access contact list use /contacts url in your web browser
To send simple message

.. code:: shell
   
    curl -XPOST 'http://<your server ip>/api/telegram/send?to=<phone number>&messag=Hello+World'

To send file content as message

.. code:: shell

   curl -XPOST -d @/path/to/file.txt 'http://<your server ip>/api/telegram/send?to=<phone number>'

Note! File may be base64 encoded

To send JSON

.. code:: shell

     curl -H 'Content-Type: application/json' -XPOST -d '{ "to": "<phone number>", "message": "Hello world"}' 'http://<your server ip>/api/telegram/sendJSON'
