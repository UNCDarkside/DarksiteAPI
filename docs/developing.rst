#######################
Development Environment
#######################

As a Python project, there are certain steps we recommend for setting up your developer environment.


*****************
Recommended Setup
*****************

These steps will walk you through setting up our recommended developer environment.

+++++++
Tooling
+++++++

The following tools are required for our recommended environment setup:

1. Python 3.6
2. Pip
3. Pipenv

+++++++++++
Source Code
+++++++++++

The first step is to clone the source code from GitHub. You can clone the project using SSH or over HTTPS.

.. code-block:: bash

    # Over SSH (Recommended)
    git clone git@github.com:UNCDarkside/DarksiteAPI

Or,

.. code-block:: bash

    # Over HTTPS
    git clone https://github.com/UNCDarkside/DarksiteAPI

Once you have the source code, ``cd`` into the repository.

.. code-block:: bash

    cd DarksiteAPI

+++++++++++++++++
Local Environment
+++++++++++++++++

Our project requires a few environment variables to work correctly. We can set these properties in a ``.env`` file that is read before executing any ``pipenv`` command.

.. code-block:: bash

    # .env
    DJANGO_DEBUG=true
    DJANGO_MEDIA_ROOT=/path/to/your/clone/darksite/media

++++++++++++++++++++
Install Dependencies
++++++++++++++++++++

We use Pipenv to manage our dependencies. We recommend installing all the development requirements, but if you only want to run the project locally you can omit the ``--dev`` flag.

.. code-block:: bash

    pipenv install --dev

++++++++++
Code Style
++++++++++

We use a combination of `black` and `flake8` to ensure the code style for the project is consistent. These tools are used by our CI process to check every pushed commit. To ensure code is well-formatted before we push it, we use the `pre-commit` tool. After installing it, it will format your code on every commit.

.. code-block:: bash

    pipenv run pre-commit install


*******************
Running the Project
*******************

To run the application locally, run the database migrations and then start the application.

.. code-block:: bash

    pipenv run darksite/manage.py migrate
    pipenv run darksite/manage.py runserver

This will launch the application locally on ``http://localhost:8000``.

.. note::

    You must run the ``migrate`` command whenever additional migrations are added to the source. The ``runserver`` command will log a warning if you forget to do this, and any new logic relying on the presence of the new tables will cause crashes.

++++++++++++++++
First Time Setup
++++++++++++++++

The first time you run the project, you will want to create a super-user that you can use to access the admin interface.

.. code-block:: bash

    pipenv run darksite/manage.py createsuperuser
