from setuptools import setup, find_packages

setup(
    name="fibrosisoptimization",
    description=(""),
    version="0.1",
    packages=find_packages(exclude=["examples", "simulations"]),
    install_requires=["numpy", "scipy", "matplotlib"]
)
