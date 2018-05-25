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

.. code:: shell

    git clone https://github.com/scorp251/teleapi

Getting Started
---------------

Copy file config.ini.sample to config.ini and fill requiered fields
From main directory run 
.. code:: shell

    gunicorn -b 127.0.0.1:5000 --reload app:app

Configure NGINX

.. code-block:: shell

    server {
        listen 0.0.0.0:80;

        location / {
            proxy_pass http://127.0.0.1:5000;
        }

        location /contacts/static {
            root /opt/teleapi/app;
       }
    }

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
