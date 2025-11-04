from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ip-tracker",
    version="1.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=2.0.0",
    ],
    entry_points={
        'console_scripts': [
            'ip-tracker=ip_tracker.main:main',
        ],
    },
    author="Synergy Tool",
    author_email="tool@synergy.com",
    description="Facebook-style IP Tracker with Termux UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ip tracker termux flask facebook",
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)