import os

import setuptools

requires = [
    'python-dateutil',
    'google-api-python-client',
    'oauth2client',
    'httplib2'
]

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    long_description = f.read()


def __package_files(directory):
    """
    Collect the package files.
    """
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setuptools.setup(
    name="gcalendar",
    version="0.1",
    description="Read Google Calendar events from your terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gobinath Loganathan",
    author_email="slgobinath@gmail.com",
    url="https://github.com/slgobinath/gcalendar",
    download_url="https://github.com/slgobinath/gcalendar/archive/v0.1.tar.gz",
    packages=setuptools.find_packages(),
    package_data={},
    install_requires=requires,
    entry_points={'console_scripts': ['gcalendar = gcalendar.__main__:main']},
    keywords='linux utility google-calendar',
    classifiers=[
                    "Operating System :: POSIX :: Linux",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Development Status :: 5 - Production/Stable",
                    "Environment :: X11 Applications :: GTK",
                    "Intended Audience :: End Users/Desktop",
                    "Topic :: Utilities"] + [('Programming Language :: Python :: %s' % x) for x in
                                             '3 3.4 3.5 3.6 3.7'.split()]
)
