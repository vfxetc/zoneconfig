from setuptools import setup, find_packages

setup(
    name='zoneconfig',
    version='1.0.0.dev0',
    description='Heirarchical, context-dependant, configuration system.',
    url='http://github.com/vfxetc/zoneconfig',
    
    packages=find_packages(exclude=['build*', 'tests*']),
    include_package_data=True,
    
    author='Mike Boers',
    author_email='zoneconfig@mikeboers.com',
    license='BSD-3',
    
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
)
