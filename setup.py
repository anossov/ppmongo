from setuptools import setup
import codecs

def readme(fn):
    with codecs.open(fn, encoding='utf-8') as f:
        return unicode(f.read())

setup(name='ppmongo',
    version='0.1.0',
    packages=[
            'ppmongo',
        ],
    scripts=[
            'bin/ppmongo',
        ],

    author='Pavel Anossov',
    author_email='anossov@gmail.com',

    classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Programming Language :: Python :: 2.7',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Topic :: Utilities',
            'Topic :: Database'
        ],

    url='https://github.com/anossov/ppmongo',
    license='BSD',
    description='Retrieve and pretty-print data from mongo',
    long_description=readme('README.txt'),
    install_requires=[
            'pymongo'
        ]
)
