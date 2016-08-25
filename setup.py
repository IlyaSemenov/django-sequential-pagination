"""Fast sequential objects pagination for Django"""

from setuptools import setup, find_packages


setup(
	name='django-sequential-pagination',
	version='0.0.1',
	url='https://github.com/IlyaSemenov/django-sequential-pagination',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description=__doc__,
	long_description=open('README.rst').read(),
	packages=find_packages(),
	install_requires=['Django>=1.7'],
	classifiers=[],
)
