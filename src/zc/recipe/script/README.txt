===========================
Deployment-specific scripts
===========================

Many deployments provide scripts that tie the configurations into the
software.  This is often done to make it easier to work with specific
deployments of the software.

The conventional Unix file hierarchy doesn't really provide a good
shared place for such scripts; the zc.recipe.deployment:script recipe
generates these scripts in the deployment's bin-directory, but we'd
rather have the resulting scripts associated with the deployment itself.

The options for the recipe are the same as those for the
zc.recipe.egg:script recipe, with the addition of a required deployment
setting.  The etc-directory from the deployment is used instead of the
buildout's bin-directory.  This allows deployment-specific information
to be embedded in the script via the initialization setting.

Let's take a look at a simple case.  We'll need a package with a
console_script entry point:

    >>> write('setup.py', '''\
    ... from setuptools import setup
    ... setup(
    ...     name="testpkg",
    ...     package_dir={"": "src"},
    ...     py_modules=["testmodule"],
    ...     zip_safe=False,
    ...     entry_points={
    ...         "console_scripts": [
    ...             "myscript=testmodule:main",
    ...             ],
    ...         },
    ...     )
    ... ''')

    >>> mkdir('src')
    >>> write('src', 'testmodule.py', '''\
    ... some_setting = "42"
    ... def main():
    ...     print some_setting
    ... ''')

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts = somescript
    ...
    ... [mydep]
    ... recipe = zc.recipe.deployment
    ... prefix = %s
    ... user = %s
    ... etc-user = %s
    ...
    ... [somescript]
    ... recipe = zc.recipe.script
    ... deployment = mydep
    ... eggs = testpkg
    ... scripts = myscript
    ... initialization =
    ...     import testmodule
    ...     testmodule.some_setting = "24"
    ... ''' % (sample_buildout, user, user))

    >>> print system(join('bin', 'buildout')), # doctest: +NORMALIZE_WHITESPACE
    Develop: 'PREFIX/.'
    Installing mydep.
    zc.recipe.deployment:
        Creating 'PREFIX/etc/mydep',
        mode 755, user 'USER', group 'GROUP'
    zc.recipe.deployment:
        Creating 'PREFIX/var/log/mydep',
        mode 755, user 'USER', group 'GROUP'
    zc.recipe.deployment:
        Creating 'PREFIX/var/run/mydep',
        mode 750, user 'USER', group 'GROUP'
    zc.recipe.deployment:
        Creating 'PREFIX/etc/cron.d',
        mode 755, user 'USER', group 'GROUP'
    zc.recipe.deployment:
        Creating 'PREFIX/etc/init.d',
        mode 755, user 'USER', group 'GROUP'
    zc.recipe.deployment:
        Creating 'PREFIX/etc/logrotate.d',
        mode 755, user 'USER', group 'GROUP'
    Installing somescript.
    Generated script 'PREFIX/etc/mydep/myscript'.

    >>> print ls("etc/mydep")
    drwxr-xr-x USER GROUP etc/mydep

    >>> cat("etc/mydep/myscript") # doctest: +NORMALIZE_WHITESPACE
    #!/home/fdrake/local/bin/python2.6
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
        'PREFIX/src',
        ]
    <BLANKLINE>
    import testmodule
    testmodule.some_setting = "24"
    <BLANKLINE>
    import testmodule
    <BLANKLINE>
    if __name__ == '__main__':
        testmodule.main()
