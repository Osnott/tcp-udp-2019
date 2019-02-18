import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udp-client-osnott",
    version="0.1.0",
    author="Aiden Onstott",
    author_email="aidenonstott@gmail.com",
    description="UDP Client package for team 6479",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Osnott/tcp-udp-2019",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
