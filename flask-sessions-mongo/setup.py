from setuptools import setup

setup(
    name = "Flask-Sessions-Mongo",
    version = "0.0.1",
    author = "Andrey Khobnya",
    author_email = "andrey@khobnya.me",
    description = "MongoDB backend for flask server-side sessions",
    license = "MIT",
    keywords = "session, adapter, storage, flask, mongo",
    py_modules=['flask_sessions_mongo'],
    install_requires=[
        'Flask',
        'Flask-PyMongo',
        'M2Crypto',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)