##############################################################################
#
# Copyright (c) 2011 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Visible Source 
# License, Version 1.0 (ZVSL).  A copy of the ZVSL should accompany this 
# distribution.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Create scripts that live in a deployment.

"""

import zc.recipe.egg


class Script(zc.recipe.egg.Scripts):

    def __init__(self, buildout, name, options):
        options["relative-paths"] = "false"
        deployment = buildout[options["deployment"]]
        directory = deployment["etc-directory"]
        super(Script, self).__init__(buildout, name, options)
        self.options["bin-directory"] = directory
        # The base class initializes this, so we fix it up.
        self.options["_b"] = directory
