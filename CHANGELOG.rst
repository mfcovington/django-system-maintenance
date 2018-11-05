Revision History
================

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
