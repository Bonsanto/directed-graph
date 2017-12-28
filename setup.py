import re
from setuptools import setup, find_packages


# Get version without importing, which avoids dependency issues
def get_version():
    with open('directedgraph/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


def readme():
    with open('README.md') as f:
        return f.read()

install_requires = ['pandas', 'networkx']

setup(
    name='directedgraph',
    version=get_version(),
    author='Alberto Bonsanto',
    author_email='',
    url='https://github.com/Bonsanto/directed-graph',
    description='Wrapper over Networkx Digraph',
    long_description=readme(),
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['graph', 'subgraph', 'subset', 'disjointsubset', 'directed-graph'],
)
