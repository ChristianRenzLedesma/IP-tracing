from setuptools import setup, find_packages

setup(
    name="ip-tracker",
    version="1.0.0",
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
    description="Facebook-style IP Tracker for Termux/Linux",
    keywords="ip tracker termux flask",
    python_requires='>=3.6',
)