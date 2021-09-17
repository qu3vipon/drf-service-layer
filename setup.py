import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

extras_require = {
    'test': [
        'pytest-cov',
        'pytest-django',
        'pytest',
        'tox',
    ],
    'lint': [
        'flake8',
        'pep8',
        'isort',
    ],
}

# This call to setup() does all the work
setup(
    name="drf-service-layer",
    version="0.0.1",
    description="Simple package supports service-layered design for Django REST Framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/qu3vipon/drf-service-layer",
    author="qu3vipon",
    author_email="qu3vipon@gmail.com",
    license="MIT",
    keywords=["django", "drf", "service", "layer", "service-layer"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=[
        'django',
        'djangorestframework',
    ],
    python_requires='>=3.7',
    extras_require=extras_require,
)
