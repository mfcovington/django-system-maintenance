import os
import sys
from setuptools import setup

if sys.version_info < (3, 4):
    print("Sorry, django-system-maintenance currently requires Python 3.4+.")
    sys.exit(1)

# From: https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    "Django>=2.0,<3.0",    # Confirmed good through 2.1.3
    "django-markupfield-helpers>=0.1.1",    # Confirmed good through 0.1.1
    "django-project-home-templatetags>=0.1.0",    # Confirmed good through 0.1.0
]

setup(
    name='django-system-maintenance',
    version='0.4.4',
    packages=['system_maintenance'],
    include_package_data=True,
    license='BSD License',
    keywords='sysadmin system administration documentation maintenance',
    description='A Django app to document and track the administration and maintenance of computer systems',
    long_description=(read('README.rst') + '\n\n' +
                      read('CHANGELOG.rst')),
    url='https://github.com/mfcovington/django-system-maintenance',
    author='Michael F. Covington',
    author_email='mfcovington@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: System :: Systems Administration',
    ],
    install_requires=install_requires,
)
