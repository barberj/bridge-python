from distutils.core import setup

setup(
    name='FlotypeBridge',
    version='0.1.0',
    author='Flotype Inc.',
    author_email='team@flotype.com',
    packages=['flotype'],
    url='http://pypi.python.org/pypi/FlotypeBridge/',
    license='LICENSE.txt',
    description='A Python API for the Flotype Bridge service.',
    long_description=open('README.txt').read(),
    install_requires=[
        "tornado >= 2.2",
    ]
)
