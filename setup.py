import setuptools

from fedwire import __version__ as version

with open('CHANGELOG.md') as f:
    history = f.read()

description = 'A python package that implements an interface to read/write files for the Fedwire Funds Service'

setuptools.setup(
        name='fedwire',
        version=version,
        description='{0}\n\n{1}'.format(description, history),
        author='Narmitech',
        author_email='support@naritech.com',
        url='https://github.com/narmitech/fedwire-python',
        install_requires=[
            # 'bryl==0.1.0'
        ],
        packages=['fedwire'],
        license='Apache 2.0'
)
