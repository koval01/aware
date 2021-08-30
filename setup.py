from setuptools import setup

setup(
    name='awse_site',
    version='1.0',
    packages=['awse', 'awse.migrations', 'awse.news_utils', 'awse.search_utils', 'awse_web'],
    url='https://www.awse.us/',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Koval Yaroslav',
    author_email='koval@q-writer.com',
    description='AWSE - Search engine'
)
