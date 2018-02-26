Installing Jarbas
=================

Settings
--------

Copy ``contrib/.env.sample`` as ``.env`` in the project's root folder and adjust your settings. These are the main variables:

Django settings
~~~~~~~~~~~~~~~

-  ``DEBUG`` (*bool*) enable or disable `Django debug mode <https://docs.djangoproject.com/en/1.10/ref/settings/#debug>`__
-  ``GOSS_VERSION`` (*str*) `Version for Goss tester in Docker <https://goss.rocks>`__
-  ``SECRET_KEY`` (*str*) `Django's secret key <https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-SECRET_KEY>`__
-  ``ALLOWED_HOSTS`` (*str*) `Django's allowed hosts <https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts>`__
-  ``USE_X_FORWARDED_HOST`` (*bool*) `Whether to use the ``X-Forwarded-Host`` header <https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-USE_X_FORWARDED_HOST>`__
-  ``CACHE_BACKEND`` (*str*) `Cache backend <https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-CACHES-BACKEND>`__ (e.g. ``django.core.cache.backends.memcached.MemcachedCache``)
-  ``CACHE_LOCATION`` (*str*) `Cache location <https://docs.djangoproject.com/en/1.10/ref/settings/#location>`__ (e.g. ``localhost:11211``)
-  ``SECURE_PROXY_SSL_HEADER`` *(str)* `Django secure proxy SSL header <https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header>`__ (e.g. ``HTTP_X_FORWARDED_PROTO,https`` transforms in tuple ``('HTTP_X_FORWARDED_PROTO', 'https')``)

Database
~~~~~~~~

-  ``DATABASE_URL`` (*string*) `Database URL <https://github.com/kennethreitz/dj-database-url#url-schema>`__, must be `PostgreSQL <https://www.postgresql.org>`__ since Jarbas uses `JSONField <https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#jsonfield>`__.

Message Broker
~~~~~~~~~~~~~~

-  ``CELERY_BROKER_URL`` (*string*) `Celery <http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html>`__ compatible message broker URL (e.g. ``amqp://guest:guest@localhost//``)

Amazon S3 settings
~~~~~~~~~~~~~~~~~~

-  ``AMAZON_S3_BUCKET`` (*str*) Name of the Amazon S3 bucket to look for datasets (e.g. ``serenata-de-amor-data``)
-  ``AMAZON_S3_REGION`` (*str*) Region of the Amazon S3 (e.g. ``s3-sa-east-1``)
-  ``AMAZON_S3_CEAPTRANSLATION_DATE`` (*str*) File name prefix for dataset guide (e.g. ``2016-08-08`` for ``2016-08-08-ceap-datasets.md``)

Google settings
~~~~~~~~~~~~~~~

-  ``GOOGLE_ANALYTICS`` (*str*) Google Analytics tracking code (e.g. ``UA-123456-7``)
-  ``GOOGLE_STREET_VIEW_API_KEY`` (*str*) Google Street View Image API key

Twitter settings
~~~~~~~~~~~~~~~~

-  ``TWITTER_CONSUMER_KEY`` (*str*) Twitter API key
-  ``TWITTER_CONSUMER_SECRET`` (*str*) Twitter API secret
-  ``TWITTER_ACCESS_TOKEN`` (*str*) Twitter access token
-  ``TWITTER_ACCESS_SECRET`` (*str*) Twitter access token secret

To get this credentials follow ```python-twitter`` instructions <https://python-twitter.readthedocs.io/en/latest/getting_started.html#getting-your-application-tokens>`__.

NewRelic settings
~~~~~~~~~~~~~~~~~

-  ``NEW_RELIC_APP_NAME`` (*str*) `The name of the application you wish to report data against in the New Relic UI. If not defined, this defaults to ``Python Application`` <https://docs.newrelic.com/docs/agents/python-agent/configuration/python-agent-configuration#app_name>`__ (e.g. ``Jarbas``)
-  ``NEW_RELIC_ENVIRONMENT`` (*str*) `The name of a specific deployment environment <https://docs.newrelic.com/docs/agents/python-agent/configuration/python-agent-configuration#config-file-deployment-environments>`__ (e.g. ``Production``)
-  ``NEW_RELIC_LICENSE_KEY`` (*str*) `Specifies the license key of your New Relic account. This key associates your app's metrics with your New Relic account. <https://docs.newrelic.com/docs/agents/python-agent/configuration/python-agent-configuration#license_key>`__
-  ``NEW_RELIC_DEVELOPER_MODE`` (*str*) (e.g. true or false)

For the production environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``VIRTUAL_HOST_WEB`` (*str*) host used for the HTTPS certificate (for testing production settings locally you might need to add this host name to your ``/etc/hosts``)
-  ``LETSENCRYPT_EMAIL`` (*str*) Email used to create the HTTPS certificate at Let's Encrypt
-  ``HTTPS_METHOD`` (*str*) if set to ``noredirect`` does **not** redirect from HTTP to HTTPS (default: ``redirect``)

Using Docker
------------

There are two combinations in terms of With `Docker <https://docs.docker.com/engine/installation/>`__ and `Docker Compose <https://docs.docker.com/compose/install/>`__ environments.

-  **Develoment**: simply running ``docker-compose …`` will trigger ``docker-compose.yml`` and ``docker-compose.override.yml`` with optimun configuration for developing such as:
-  automatic serving static files through Django
-  restarting the Django on Python files changes
-  rebuilding JS from Elm files on save
-  skipping server cache
-  **Production**: passing a specific configurarion as ``docker-compose -f docker-compose.yml -f docker-compose.prod.yml …`` will launch a more robust environment with production in mind, among others:
-  ``nginx`` in front of Django
-  server-side cache with memcached
-  manually generate JS after edits on Elm files
-  manually run ``collectstatic`` command is static changes
-  manually restarting server on change
-  requires ``VIRTUAL_HOST_WEB`` envvar, e.g. ``VIRTUAL_HOST_WEB=jarbas.serenata.ai docker-compose -f docker-compose.yml -f docker-compose.prod.yml …``

That said instructions here keep it simple and runs with the development set up. To swicth always add ``-f docker-compose.yml -f docker-compose.prod.yml`` after ``docker-compose``.

When using tghe production settings remember to double check the `appropriate environment varables <#for-the-production-environment>`__ and to create a ``.env.prod`` (separate from ``.env``) to hold production only values.

Build and start services
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    $ docker-compose up -d

Create and seed the database with sample data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating the database and applying migrations:

::

    $ docker-compose run --rm django python manage.py migrate

Seeding it with sample data:

.. code:: console

    $ docker-compose run --rm django python manage.py reimbursements /mnt/data/reimbursements_sample.xz
    $ docker-compose run --rm django python manage.py companies /mnt/data/companies_sample.xz
    $ docker-compose run --rm django python manage.py suspicions /mnt/data/suspicions_sample.xz
    $ docker-compose run --rm django python manage.py tweets

If you're interesting in having a database full of data you can get the datasets running `Rosie <https://github.com/datasciencebr/rosie>`__. To add a fresh new ``reimbursements.xz`` or ``suspicions.xz`` brewed by `Rosie <https://github.com/datasciencebr/rosie>`__, or a ``companies.xz`` you've got from the `toolbox <https://github.com/datasciencebr/serenata-toolbox>`__, you just need copy these files to ``contrib/data`` and refer to them inside the container from the path ``/mnt/data/``.

Creating search vector
~~~~~~~~~~~~~~~~~~~~~~

For text search in the dashboard:

.. code:: console

    $ docker-compose run --rm django python manage.py searchvector

Acessing Jabas
~~~~~~~~~~~~~~

You can access it at ```localhost:8000`` <http://localhost:8000/>`__ in development mode or ```localhost`` <http://localhost:80/>`__ in production mode.

To change any of the default environment variables defined in the ``docker-compose.yml`` just export it in a local environment variable, so when you run Jarbas it will get them.

Docker Ready?
~~~~~~~~~~~~~

Not sure? Test it!

.. code:: console

    $ docker-compose run --rm django python manage.py check
    $ docker-compose run --rm django python manage.py test

Local install
-------------

Requirements
~~~~~~~~~~~~

Jarbas requires `Python 3.5 <http://python.org>`__, `Node.js 8 <https://nodejs.org/en/>`__, `RabbitMQ 3.6 <https://www.rabbitmq.com>`__, and `PostgreSQL 9.6 <https://www.postgresql.org>`__. Once you have ``pip`` and ``npm`` available install the dependencies:

.. code:: console

    $ npm install
    $ ./node_modules/.bin/elm-package install --yes  # this might not be necessary https://github.com/npm/npm/issues/17316
    $ python -m pip install -r requirements-dev.txt

Python's ``lzma`` module
^^^^^^^^^^^^^^^^^^^^^^^^

In some Linux distros ``lzma`` is not installed by default. You can check whether you have it or not with ``$ python -m lzma``. In Debian based systems you can fix that with ``$ apt-get install liblzma-dev`` or in macOS with ``$ brew install xz`` — but you might have to re-compile your Python.

Setup your environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basically this means copying ``contrib/.env.sample`` as ``.env`` in the project's root folder — but there is `an entire section on that <#settings>`__.

Migrations
~~~~~~~~~~

Once you're done with requirements, dependencies and settings, create the basic database structure:

.. code:: console

    $ python manage.py migrate

Load data
~~~~~~~~~

To load data you need RabbitMQ running and a Celery worker:

::

    $ celery worker --app jarbas

Now you can load the data from our datasets and get some other data as static files:

::

    $ python manage.py reimbursements <path to reimbursements.xz>
    $ python manage.py suspicions <path to suspicions.xz file>
    $ python manage.py companies <path to companies.xz>
    $ python manage.py tweets
    $ python manage.py ceapdatasets

There are sample files to seed yout database inside ``contrib/data/``. You can get full datasets running `Rosie <https://github.com/datasciencebr/rosie>`__ or directly with the `toolbox <https://github.com/datasciencebr/serenata-toolbox>`__.

Creating search vector
~~~~~~~~~~~~~~~~~~~~~~

For text search in the dashboard:

.. code:: console

    $ python manage.py searchvector

Generate static files
~~~~~~~~~~~~~~~~~~~~~

We generate assets through NodeJS, so run it before Django collecting static files:

.. code:: console

    $ npm run assets
    $ python manage.py collectstatic

Ready?
~~~~~~

Not sure? Test it!

::

    $ python manage.py check
    $ python manage.py test

Ready!
~~~~~~

Run the server with ``$ python manage.py runserver`` and load `localhost:8000 <http://localhost:8000>`_ in your favorite browser.
