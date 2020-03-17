import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="huik-module", # Replace with your own username this is for PIP install, not the real python package name. the real name will be example_pkg
    version="0.0.2",
    author="Hui Kang",
    author_email="rocksnow1942@gmail.com",
    description="Modules for my scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rocksnow1942/mymodule",
    packages=setuptools.find_packages(), # or can manually enter.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['psutil'],
    python_requires='>=3.6',
)

