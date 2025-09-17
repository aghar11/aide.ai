from setuptools import setup, find_packages

setup(
    name="aide-ai",
    version="0.1.0",
    description="aide.ai — CLI-first AI OS Agent (prototype)",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "httpx",
        "python-dotenv",
        "click",
        "psutil",
        "pydantic",
        "openai",
        "python-magic",
    ],
    entry_points={
        "console_scripts": [
            "aide=aide_cli_entry:main",  # will create a thin wrapper module below
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)