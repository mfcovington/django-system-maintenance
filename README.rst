*************************
django-system-maintenance
*************************

``django-system-maintenance`` is a Django app to document and track the administration and maintenance of computer systems.

Source code is available on GitHub at `mfcovington/django-system-maintenance <https://github.com/mfcovington/django-system-maintenance>`_.

.. contents:: :local:


.. Installation
.. ============

.. **PyPI**

.. .. code-block:: sh

..     pip install django-system-maintenance

.. **GitHub**

.. .. code-block:: sh

..     pip install https://github.com/mfcovington/django-system-maintenance/releases/download/0.0.0/django-system-maintenance-0.0.0.tar.gz


Configuration
=============

Add ``system_maintenance`` and its dependencies to ``INSTALLED_APPS``in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django.contrib.humanize',
        'system_maintenance',
    )

Add the ``system_maintenance`` URLs to the site's ``urls.py``:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^system_maintenance/', include('system_maintenance.urls', namespace='system_maintenance')),
    ]


Migrations
==========

Create and perform ``system_maintenance`` migrations:

.. code-block:: sh

    python manage.py makemigrations system_maintenance
    python manage.py migrate


Usage
=====

- Start the development server:

.. code-block:: sh

    python manage.py runserver


- Login and add yourself as a system administrator: ``http://localhost:8000/admin/system_maintenance/sysadmin/add/``
- Visit: ``http://127.0.0.1:8000/system_maintenance/``


*Version 0.0.0*
