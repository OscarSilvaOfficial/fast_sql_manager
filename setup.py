import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fast_sql_manager",
    version="1.2.3",
    author="Oscar da Silva",
    author_email="oscarkaka222@gmail.com",
    description="Um pacote simples para realizar operações no banco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OscarSilvaOfficial/fast_sql_manager",
    packages=setuptools.find_packages(),
    install_requires=[
        'mysql-connector-python>=8.0.27',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)