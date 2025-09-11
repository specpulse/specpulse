"""
SpecPulse Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="specpulse",
    version="1.0.0",
    author="SpecPulse",
    author_email="",
    description="Next-Generation Specification-Driven Development Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/specpulse",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0",
        "rich>=13.0",
        "jinja2>=3.0",
        "gitpython>=3.1",
        "toml>=0.10",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "pre-commit>=3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "specpulse=specpulse.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "specpulse": [
            "resources/templates/*.md",
            "resources/memory/*.md",
            "resources/scripts/*.sh",
            "resources/commands/claude/*.md",
            "resources/commands/gemini/*.toml",
        ],
    },
    zip_safe=False,
)