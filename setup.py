import setuptools

description = "Standard development tooling for Bocadillo"

with open("README.md", "r") as readme:
    long_description = readme.read()

GITHUB = "https://github.com/bocadilloproject/bocadillo-cli"
CHANGELOG = f"{GITHUB}/blob/master/CHANGELOG.md"

setuptools.setup(
    name="bocadillo-cli",
    version="0.0.1",
    author="Florimond Manca",
    author_email="florimond.manca@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["bocadillo=main:cli"]},
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
