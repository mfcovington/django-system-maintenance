Revision History
================

0.4.5 2018-12-13

- Remove ``MarkupField`` args already defined by markupfield helper


0.4.4 2018-12-06

- DRY up with markupfield_helpers


0.4.3 2018-12-06

- Include migrations when packaging for distribution


0.4.2 2018-11-26

- Add ``django-project-home-templatetags`` compatibility for breadcrumbs
- Include tests in distribution


0.4.1 2018-11-05

- Make compatible with Django 2.1
- Python>=3.4; Django>=2.0,<3.0


0.4.0 2018-11-05

- Make compatible with Django 2.0
- Drop Python 3.2 and 3.3 compatibility
- Python>=3.4; Django>=2.0,<=2.0.9


0.3.2 2018-11-05

- Set upper bound of <2.0 for Django version
- Python>=3.2,<3.8; Django>=1.7,<2.0
- Final version that will be compatible with Django 1.11.16


0.3.1 2018-11-05

- Prepare for upgrade to Django 2+
- Update dependency version requirements


0.3.0 2018-11-04

- Add unit tests and functional tests
- Add links to view raw markdown
- Update configuration instructions in README
- Set next page to System Maintenance home page if accessing authentication page directly
- Fix maintenance record status so it defaults to 'In Progress'
- Resolve Django 1.10 deprecation warnings
- DRY and simplify


0.2.0 2015-12-12

- Redirect to sysadmin authentication page instead of 404 if current user is not a sysadmin
- Make pagination customizable via ``settings.SYSTEM_MAINTENANCE_PAGINATE_BY``
- Open System Maintenance admin page in a new tab
- Add missing imports for plain text markup fields
- Add installation instructions to README
- Add default app configuration


0.1.0 2015-11-02

- A Django app to document and track the administration and maintenance of computer systems
