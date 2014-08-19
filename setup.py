import os.path
from setuptools import setup, find_packages

name = 'zc.recipe.script'

entry_points = '''\
[zc.buildout]
default = %(name)s:Script
''' % globals()

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version='1.0.2',
    author='Fred Drake',
    author_email='fred@zope.com',
    description='zc.buildout recipe for scripts in Unix deployments',
    license='ZVSL',
    keywords='deployment build',
    url='http://svn.zope.com/repos/main/%s/' % name,
    long_description=(
        read('src', 'zc', 'recipe', 'script', 'README.txt')
        + "\n\n" +
        read('README.rst')
        ),
    classifiers=[
        "Framework :: Buildout :: Recipe",
        ],
    install_requires=['setuptools', 'zc.recipe.egg'],
    extras_require={
        'test': [
            'zc.buildout',
            'zc.recipe.deployment',
            'zope.testing',
            ],
        },
    package_data={
        'zc.recipe.script': ['*.txt'],
        },
    entry_points=entry_points,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    namespace_packages=['zc', 'zc.recipe'],
    zip_safe=False,
    include_package_data=True,
    )
