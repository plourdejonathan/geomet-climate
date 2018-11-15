###############################################################################
#
# Copyright (C) 2018 Tom Kralidis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import io
import os
import re
from setuptools import Command, find_packages, setup
import shutil
import sys


class PyCleanBuild(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        remove_files = [
            'debian/files',
            'debian/geomet-climate.debhelper.log',
            'debian/geomet-climate.postinst.debhelper',
            'debian/geomet-climate.prerm.debhelper',
            'debian/geomet-climate.substvars'
        ]

        remove_dirs = [
            'debian/geomet-climate'
        ]

        for file_ in remove_files:
            try:
                os.remove(file_)
            except OSError:
                pass

        for dir_ in remove_dirs:
            try:
                shutil.rmtree(dir_)
            except OSError:
                pass

        for file_ in os.listdir('..'):
            if file_.endswith(('.deb', '.build', '.changes')):
                os.remove('../{}'.format(file_))


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        errno = subprocess.call([sys.executable,
                                 'geomet_climate/tests/run_tests.py'])
        raise SystemExit(errno)


class PyCoverage(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess

        errno = subprocess.call(['coverage', 'run', '--source=geomet_climate',
                                 '-m', 'unittest',
                                 'geomet_climate.tests.run_tests'])
        errno = subprocess.call(['coverage', 'report', '-m'])
        raise SystemExit(errno)


def read(filename, encoding='utf-8'):
    """read file contents"""
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with io.open(full_path, encoding=encoding) as fh:
        contents = fh.read().strip()
    return contents


def get_package_version():
    """get version from top-level package init"""
    version_file = read('geomet_climate/__init__.py')
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    print('Conversion to rST failed.  Using default (will look weird on PyPI)')
    LONG_DESCRIPTION = read('README.md')

if os.path.exists('MANIFEST'):
    os.unlink('MANIFEST')

setup(
    name='geomet-climate',
    version=get_package_version(),
    description='Geospatial Web Services for Canadian climate data',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    platforms='all',
    keywords=' '.join([
        'geomet',
        'climate',
    ]),
    author='Meteorological Service of Canada',
    author_email='tom.kralidis@canada.ca',
    maintainer='Meteorological Service of Canada',
    maintainer_email='tom.kralidis@canada.ca',
    url='https://github.com/ECCC-CCCS/geomet-climate',
    install_requires=read('requirements.txt').splitlines(),
    packages=find_packages(exclude=['geomet_climate.tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'geomet-climate=geomet_climate:cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    cmdclass={
        'test': PyTest,
        'coverage': PyCoverage,
        'cleanbuild': PyCleanBuild
    }
)