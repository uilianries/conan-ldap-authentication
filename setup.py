from setuptools import setup, find_packages
from codecs import open
from os.path import expanduser
"""LDAP authenticator for Conan project.

"""
__author__ = "Uilian Ries"
__license__ = "MIT"


class Requirements(object):
    __requirements_path = "conan/requirements.txt"

    @staticmethod
    def get():
        """Retrieve all dependencies for this project

        :param filename:
        :return:
        """
        requirements = []
        with open(Requirements.__requirements_path) as req_file:
            for line in req_file.read().splitlines():
                if not line.strip().startswith("#"):
                    requirements.append(line)
        return requirements


setup(
    name='conan_ldap_authentication',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.1.0",

    description='LDAP authenticator for Conan C/C++ package manager',

    # The project's main homepage.
    url='https://github.com/uilianries/conan-ldap-authentication',

    # Author details
    author='Uilian Ries',
    author_email='uilianries@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords=['conan', 'ldap', 'package', 'authentication'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=Requirements.get(),

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'conan': ['*.txt'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('%s/.conan_server/plugins/authenticatior' % expanduser('~'), ['conan/ldap_authentication.py'])],
)
