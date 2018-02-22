from setuptools import setup, find_packages

requires = [
    'requests==2.18.4',
    'Twisted==17.9.0',
]

setup(
    name='pulsar',
    version='1.0',
    url='',
    license='',
    author='Mateusz Cyraniak',
    author_email='m.cyraniak@gmail.com',
    description='',
    packages=find_packages(),
    install_requires=requires,
)
