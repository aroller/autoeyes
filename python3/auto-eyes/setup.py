import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-eyes",
    version="0.0.1",
    author="Aaron Roller",
    author_email="aaron.roller@aawhere.com",
    description="A simple lighting system for Autonomous Vehicle to Human Communications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aroller/auto-eyes",
    packages=setuptools.find_packages(),
    # https://pypi.org/project/{package name} for more docs
    install_requires=[
        'markdown',
        'connexion[swagger-ui]',
        'colour',
        'overrides'
        # 'rpi_ws281x', #  only enable in raspberry pi install
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
