from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.1'

install_requires = [
    'markdown', 'argparse',
]

setup(name='markowik',
    version=version,
    description="Convert Markdown to Google Code Wiki",
    long_description=README,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='markdown google-code wiki',
    author='Oben Sonne',
    author_email='obensonne@googlemail.com',
    url='http://pypi.python.org/pypi/markowik',
    license='MIT',
    packages=find_packages('src', exclude=['tests']),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['markowik=markowik.main:main']
    }
)
