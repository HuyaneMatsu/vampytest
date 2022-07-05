import pathlib, re
from ast import literal_eval
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# Lookup version
version_search_pattern = re.compile('^__version__[ ]*=[ ]*((?:\'[^\']+\')|(?:\"[^\"]+\"))[ ]*$', re.M)
parsed = version_search_pattern.search((HERE / 'vampytest' / '__init__.py').read_text())
if parsed is None:
    raise RuntimeError('No version found in `__init__.py`.')

version = literal_eval(parsed.group(1))

# Lookup readme
README = (HERE / 'README.md').read_text('utf-8')

setup(
    author = 'HuyaneMatsu',
    author_email = 're.ism.tm@gmail.com',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        
        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        #'Programming Language :: Python :: 3.11',
        
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description = 'A vampy test framework',
    include_package_data = True,
    install_requires = [
        'scarletio',
    ],
    license = 'DBAD',
    long_description = README,
    long_description_content_type = 'text/markdown',
    name = 'vampytest',
    packages = [
        'vampytest',
        'vampytest.core',
        'vampytest.core.assertions',
        'vampytest.core.environment',
        'vampytest.core.event_handling',
        'vampytest.core.events',
        'vampytest.core.file',
        'vampytest.core.result',
        'vampytest.core.result.failures',
        'vampytest.core.runner',
        'vampytest.core.wrappers',
        'vampytest.main',
    ],
    python_requires = '>=3.6',
    url = 'https://github.com/HuyaneMatsu/vampytest',
    version = version,
)
