from setuptools import setup, find_packages

setup(
    name="PACER",
    version="1.0",
    packages=find_packages(),
    scripts=['main.py'],
    install_requires=[
                        'networkx==2.0',
                        'numpy==1.13.3'],
    python_requires=">=3",
    authors=["Vasyl Borsuk", "Ivan Kosarevych"],
    authors_emails=["borsuk@ucu.edu.ua", "kosarevych@ucu.edu.ua"],
    keywords="pacer poi topk routes submodular maximization",
)