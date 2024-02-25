from setuptools import find_packages, setup


def load_requirements(fname):
    with open(fname, "r") as reqs:
        return reqs.read().splitlines()


setup(
    name="octoduck",
    version="0.1",
    description="CLI tool for downloading GitHub Archive data and loading into DuckDB.",
    author="Gwen Windflower",
    author_email="gwenwindflower@gmail.com",
    url="https://github.com/gwenwindflower/octoduck",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_dir={"octoduck": "octoduck"},
    install_requires=load_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "octoduck=octoduck.main:app",
        ],
    },
)
