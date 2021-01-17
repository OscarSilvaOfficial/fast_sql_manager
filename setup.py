import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fast_sql_manager",
    version="0.1.5",
    author="Oscar da Silva",
    author_email="oscarkaka222@gmail.com",
    description="Um pacote simples para realizar operações no banco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OscarSilvaOfficial/easy_sql",
    packages=setuptools.find_packages(),
    install_requires=[
        'six>=1.15.0',
        'mysqlclient>=2.0.3',
        'mysql-connector-python>=8.0.22',
        'mysql>=0.0.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)