#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, os
from Cheetah.Template import Template
import constructor


if __name__ == "__main__":
    import sys
    import runpy
    import os
    if len(sys.argv) != 4:
        print("Usage: bootstrap.py <recipe> <from_root> <to_root>")
    print("Bootstrapper is now cooking '" + sys.argv[1] + "' for you.")
    context = {"from_root" : sys.argv[2] , "to_root": sys.argv[3] }

    if not os.path.exists(context["to_root"]):
        os.makedirs(context["to_root"])

    l=runpy.run_path(sys.argv[1], context)
    constructor.runRefactoring(l["command"])
    print("")
