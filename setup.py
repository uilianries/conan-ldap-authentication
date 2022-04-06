from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from codecs import open
import os
import shutil
"""LDAP authenticator for Conan project.

"""
__author__ = "Uilian Ries"
__license__ = "MIT"


class Path(object):

    @staticmethod
    def home():
        username = os.getenv("SUDO_USER", None)
        home_path = '~%s' % username if username else '~'
        return os.path.expanduser(home_path)


class Requirements(object):
    __requirements_path = "conan_ldap/requirements.txt"

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


class PostInstallCommand(install):
    """Override Install command to change plugin owner

    """
    def run(self):
        """If necessary, create plugin directory, install and change file owner

        :return: None
        """
        paths = ['.conan_server', 'plugins', 'authenticator']
        conan_path = Path.home()
        for path in paths:
            conan_path = os.path.join(conan_path, path)
            if not os.path.isdir(conan_path):
                self.__mkdir_sudo_user(conan_path)
        install.run(self)
        plugin_path = os.path.join(conan_path, 'ldap_authentication.py')
        if not os.path.exists(plugin_path):
            shutil.copy(os.path.join("conan_ldap", "ldap_authentication.py"), plugin_path)
        os.chown(plugin_path, self.__get_sudo_uid(), self.__get_sudo_gid())

    def __mkdir_sudo_user(self, path):
        """Create a directory and change owner if is running as sudo

        :param path: directory path to be created
        :return: None
        """
        os.mkdir(path)
        os.chown(path, self.__get_sudo_uid(), self.__get_sudo_gid())

    def __get_sudo_uid(self):
        """Get sudo UID from environment variables

        :return: sudo uid
        """
        return int(os.environ.get('SUDO_UID')) if 'SUDO_UID' in os.environ else os.getuid()

    def __get_sudo_gid(self):
        """Get sudo GID from environment variables

        :return: sudo gid
        """
        return int(os.environ.get('SUDO_GID')) if 'SUDO_GID' in os.environ else os.getgid()


setup(
    name='conan_ldap_authentication',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.4.0",

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
        'Development Status :: 5 - Production/Stable',
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
    data_files=[(os.path.join(Path.home(), '.conan_server', 'plugins', 'authenticator'), [os.path.join('conan_ldap', 'ldap_authentication.py')])],

    # Give access to write new files at authenticator directory
    cmdclass={'install': PostInstallCommand},
)
