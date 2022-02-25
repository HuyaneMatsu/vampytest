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

        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        #'Programming Language :: Python :: 3.11',

        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description = 'A vampy test framework',
    include_package_data = True,
    license = 'MIT',
    long_description = README,
    long_description_content_type = 'text/markdown',
    name = 'vampytest',
    package_dir={'': 'vampytest'},
    python_requires = '>=3.6',
    py_modules=["vampytest"],
    url = 'https://github.com/HuyaneMatsu/hata',
    version = version,
)
