from setuptools import setup, find_packages

setup(
    name="personal-finance-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.26.0",
        "python-dotenv>=0.19.0",
        "matplotlib>=3.5.0",
        "pytest>=7.0.0",
        "flask>=2.0.0",
        "flask-sqlalchemy>=3.0.0",
        "alembic>=1.7.0",
        "pandas>=1.3.0",
    ],
    entry_points={
        'console_scripts': [
            'finance-tracker=app.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A personal finance tracking application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/personal-finance-tracker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 