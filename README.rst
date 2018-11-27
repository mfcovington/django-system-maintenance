*************************
django-system-maintenance
*************************

``django-system-maintenance`` is a Django app to document and track the administration and maintenance of computer systems.

Source code is available on GitHub at `mfcovington/django-system-maintenance <https://github.com/mfcovington/django-system-maintenance>`_.

.. contents:: :local:


Installation
============

**PyPI**

.. code-block:: sh

    pip install django-system-maintenance


**GitHub (development branch)**

.. code-block:: sh

    pip install git+http://github.com/mfcovington/django-system-maintenance.git@develop


Configuration
=============

Add ``system_maintenance`` and its dependencies to ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django.contrib.humanize',
        'project_home_tags',
        'system_maintenance',
    )

Add the ``system_maintenance`` URLs to the site's ``urls.py``:

.. code-block:: python

    from django.urls import include, path


    urlpatterns = [
        ...
        path('system_maintenance/', include('system_maintenance.urls', namespace='system_maintenance')),
    ]


By default, lists of maintenance records, etc. are paginated with 30 records per page. This value can be customized in ``settings.py``:

.. code-block:: python

    SYSTEM_MAINTENANCE_PAGINATE_BY = 50

This app is compatible with ``django-project-home-templatetags``. Check out its `Configuration Documentation <https://github.com/mfcovington/django-project-home-templatetags#configuration>`_ if you want this app's top-level breadcrumb to link to your project's homepage. To activate ``project_home_tags`` functionality, you must define ``PROJECT_HOME_NAMESPACE`` and, optionally, ``PROJECT_HOME_LABEL`` in ``settings.py``:

.. code-block:: python

    PROJECT_HOME_NAMESPACE = 'project_name:index_view'    # Namespace of homepage
    PROJECT_HOME_LABEL = 'Homepage'    # Optional; Default is 'Home'


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


*Version 0.4.1*
