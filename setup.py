from setuptools import setup, find_namespace_packages

with open("requirements.txt", "r") as f:
    requirements = [package.replace("\n", "") for package in f.readlines()]

setup(
    name="GamesAI",
    url="https://github.com/tboulet/AI-Agents-for-Games",
    author="Timothé Boulet",
    author_email="timothe.boulet0@gmail.com",
    
    packages=find_namespace_packages(),
    # Needed for dependencies
    install_requires=requirements[1:],
    dependency_links=requirements[:1],
        # package_data={"configs": "*.yaml"},
    version="0.0.1",
    license="MIT",
    description="GamesAI is a library of AI agents for games.",
    long_description=open('README.md').read(),
)