"""Chalice route reStructuredText autodoc directive for docutils/Sphinx."""
import os.path
import re
import setuptools


def read_meta():
    """Read metadata from module."""
    fname = os.path.join(os.path.dirname(__file__), 'chalicedoc.py')
    meta = {}
    with open(fname) as fobj:
        for line in fobj:
            match = re.match(r'__(?P<key>\w+)__\s*=\s*(?P<eval>.*)', line)
            if match:
                meta[match.group('key')] = eval(match.group('eval'))

    return meta


def readme():
    """Read readme file."""
    fname = os.path.join(os.path.dirname(__file__), 'README.rst')
    with open(fname) as fobj:
        return fobj.read()


if __name__ == '__main__':
    meta = read_meta()
    setuptools.setup(
        name='chalicedoc',
        version=meta['version'],
        author='Joshua Ringer',
        author_email='josh.ringer@argomi.com',
        url='https://github.com/amaas-fintech/chalicedoc',

        py_modules=['chalicedoc'],

        license='Apache License Version 2.0',
        description=__doc__,
        long_description=readme(),
        # platforms=None,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: Sphinx :: Extension',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Documentation',
            'Topic :: Documentation :: Sphinx',
            'Topic :: Software Development :: Documentation',
        ],
        keywords='chalice docutils rst sphinx',
        # provides=[],
        # requires=[],
        # obsoletes=[],

        install_requires=[
            'docutils',
            'sphinx',
        ],
    )
