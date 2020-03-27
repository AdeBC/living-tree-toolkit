from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name='living-tree',
	version='0.0.2',
	packages=['livingTree'],
	package_data={'example_tree': ['trees/*.pkl']},
	include_package_data=True,
	install_requires=['ete3==3.1.1', 'numpy>=1.15.4', 'pandas>=0.23.4', 'treelib==1.5.5'],
	url='https://github.com/AdeBC/living-tree-toolkit',
	license='MIT',
	author='ch379',
	author_email='ch37915405887@gmail.com',
	keywords=['taxonomic tree', 'living tree', 'data structure', 'Big data optimized'],
	description='An efficient toolkit for constructing and processing taxonomic trees (abundance calculations, reading count statistics, etc.).',
	long_description=long_description,
    long_description_content_type="text/markdown",
	classifiers=[
    	'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Programming Language :: Python :: 3.7',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	]
	
)
