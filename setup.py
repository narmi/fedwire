import setuptools

from fedwire import __version__ as version

with open('CHANGELOG.md') as f:
    history = f.read()

description = 'A python package that implements an interface to' \
              'read/write files for the Fedwire Funds Service'

setuptools.setup(
        name='fedwire',
        version=version,
        description='{0}\n\n{1}'.format(description, history),
        author='Narmi',
        author_email='support@naritech.com',
        url='https://github.com/narmitech/fedwire-python',
        install_requires=[],
        extras_require={
            'dev': [
                'coverage==4.0.3',
                'flake8==3.2.1',
                'flake8-per-file-ignores',
            ]
        },
        packages=['fedwire'],
        license='Apache 2.0'
)
