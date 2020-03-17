from setuptools import setup, find_packages

setup(
    name='carim',
    version='1.0',
    packages=find_packages(),
    entry_points={'console_scripts': ['carim-setup = carim.main:main']},
    url='https://github.com/schana/dayz-server-carim',
    license='License :: OSI Approved :: Apache Software License',
    author='Nathaniel Schaaf',
    author_email='nathaniel.schaaf@gmail.com',
    description='Configuration and Automation for the Carim DayZ server'
)
