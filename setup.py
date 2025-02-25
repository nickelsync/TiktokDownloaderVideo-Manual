from setuptools import setup, find_packages

setup(
    name="tiktok-downloader-watermark",
    version="0.1.0",
    description="TikTok Video Downloader watermark",
    author="Nickel",
    author_email="nickellodeoon@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "tqdm>=4.62.3",
    ],
    entry_points={
        "console_scripts": [
            "tiktok-downloader=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)