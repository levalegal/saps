from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="employee-directory",
    version="1.0.0",
    author="Student",
    description="Каталог контактов сотрудников",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/employee-directory",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
    ],
    python_requires='>=3.8',
    install_requires=[
        'PyQt6>=6.6.0',
        'qrcode>=7.4.2',
        'Pillow>=10.1.0',
        'pandas>=2.1.3',
        'openpyxl>=3.1.2',
        'reportlab>=4.0.7',
    ],
    entry_points={
        'console_scripts': [
            'employee-directory=main:main',
        ],
    },
)




