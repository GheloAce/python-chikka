try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="python-chikka",
    version="0.5.1",
    description="Python API Wrapper for Chikka ",
    author="Mark Allan B Meriales",
    author_email="mark.meriales@gmail.com",
    packages=['chikka'],
    install_requires=['requests>=2.0.1'],
    url="https://github.com/makmac213/python-chikka/",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'License :: Freeware',
    ),
    download_url="https://github.com/makmac213/python-chikka/",
)
