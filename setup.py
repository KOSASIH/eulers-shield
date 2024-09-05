from setuptools import setup, find_packages

def read_description():
    with open('README.md', 'r') as f:
        return f.read()

def get_version():
    with open('eulers_shield/__init__.py', 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'")

setup(
    name='eulers-shield',
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        'web3==5.24.0',
        'requests==2.26.0',
        'pandas==1.3.5',
        'numpy==1.22.2'
    ],
    author='KOSASIH',
    author_email='[kosasihg88@gmail.com](mailto:kosasihg88@gmail.com)',
    description='A high-tech shield for Euler\'s number',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/blackbox-ai/eulers-shield',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    keywords='eulers shield pi coin stability fund market oracle',
    project_urls={
        'Documentation': 'https://eulers-shield.readthedocs.io',
        'Source': 'https://github.com/blackbox-ai/eulers-shield',
        'Tracker': 'https://github.com/blackbox-ai/eulers-shield/issues'
    }
)
