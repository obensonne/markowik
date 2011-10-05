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
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
    keywords='markdown google-code wiki converter',
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
