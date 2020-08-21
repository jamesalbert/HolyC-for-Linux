from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='secularize',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.0.1-7',

    description='run HolyC source on linux',
    long_description=long_description,  #this is the
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://www.github.com/jamesalbert/HolyC-for-Linux',

    # Author details
    author='jamesalbert',
    author_email='jamesrobertalbert@gmail.com',

    # Choose your license
    license='MIT',

    entry_points={
       'console_scripts': [
           'secularize = secularize.__init__:main',
       ],
    },

    install_requires=['pycparser', 'docopt'],

    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='holyc linux terry lord temple mlg',

    packages=["secularize"],

)
