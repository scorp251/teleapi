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

.. code:: shell
    server {
        listen 0.0.0.0:80;

        location / {
            proxy_pass http://127.0.0.1:5000;
        }

        location /contacts/static {
            root /opt/teleapi/app;
       }
    }
