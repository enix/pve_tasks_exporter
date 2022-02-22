from setuptools import find_packages
from setuptools import setup

setup(
    name="prometheus-pve-tasks-exporter",
    version="0.0.1",
    author="Aurélien Dunand",
    author_email="aurelien.dunand@enix.fr",
    description=("Proxmox VE tasks exporter for the Prometheus monitoring system."),
    #  long_description=open('README.rst').read(),
    license="Apache Software License 2.0",
    keywords="prometheus exporter network monitoring proxmox",
    #  url="https://github.com/prometheus-pve/prometheus-pve-exporter",
    package_dir={"": "src"},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'pve_tasks_exporter=pve_tasks_exporter.cli:main',
        ],
    },
    python_requires=">=3.4",
    install_requires=[
        "prometheus_client>=0.0.11",
        "proxmoxer",
        "pyyaml",
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
    ],
)
