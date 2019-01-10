.. _testing:

#######
Testing
#######

This project has a comprehensive test suite used to ensure correctness. The test suite is run using `pytest`_.


****************
Functional Tests
****************

Functional, or end-to-end (E2E), tests are arguably the most important tests we have in the project. As a general rule, we write a functional test to cover each use case a consumer of the API would have. The role of these tests is to ensure that these use cases are runnable while making no assumptions about the internal workings of the application. Because these tests do not have any knowledge of internal workings, they are not designed to cover every edge case.

.. note::

    The required functional tests for a feature can typically be pulled from the "Acceptance Tests" section of the related GitHub issue.

These E2E tests are placed in the :file:`darksite/functional_tests/` directory. This directory is organized loosely by "feature" and is not necessarily correlated to the organization of the apps that make up the Django project.

Since these tests take much longer to run than the unit tests, they must be targeted specifically in order to run them.

.. code-block:: bash

    pipenv run pytest darksite/functional_tests/


**********
Unit Tests
**********

Each component of the project also has its own unit tests. These tests are much smaller than the functional tests and cover an isolated component. Because these tests require much less setup than the E2E tests, they are useful for covering edge cases and other scenarios that may be hard to set up without some knowledge of the application implementation.

Unit tests are located in the :file:`test/` directory of each app, and are organized such that there is a directory for each module (:file:`.py` file) and each function or class has a test file.

To run the unit tests, point ``pytest`` at the :file:`darksite` directory and it will find and run all the unit tests. You can also execute a specific test file or only tests that match a certain name.

.. code-block:: bash

    # All unit tests
    pipenv run pytest darksite/

    # Unit tests from a specific file
    pipenv run pytest darksite/account/test/models/test_user_model.py

    # Tests that have "user" in their name
    pipenv run pytest -k user darksite/


.. _pytest: https://docs.pytest.org/en/latest/
