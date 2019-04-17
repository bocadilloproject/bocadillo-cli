import os
import re
import setuptools

description = "Standard development tooling for Bocadillo"

with open("README.md", "r") as readme:
    long_description = readme.read()

NAME = "bocadillo-cli"
PACKAGE = "bocadillo_cli"
GITHUB = "https://github.com/bocadilloproject/bocadillo-cli"
CHANGELOG = f"{GITHUB}/blob/master/CHANGELOG.md"
HERE = os.path.abspath(os.path.dirname(__file__))


def find_version(*parts):
    with open(os.path.join(HERE, *parts), "r") as fp:
        content = fp.read()
    version_match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", content)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name=NAME,
    version=find_version(PACKAGE, "version.py"),
    author="Florimond Manca",
    author_email="florimond.manca@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["bocadillo_cli.templates"]),
    include_package_data=True,  # see MANIFEST.in
    entry_points={"console_scripts": ["bocadillo=bocadillo_cli.main:cli"]},
    install_requires=["click>=7.0, <8.0", "jinja2>=2.10.1"],
    python_requires=">=3.6",
    url=GITHUB,
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
        "Topic :: Software Development :: Code Generators",
    ],
)
