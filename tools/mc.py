#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, os
from Cheetah.Template import Template
import sr

# def lprint(l):
    # print(json.dumps(l, indent=4, separators=(',', ':')))

# def getSourceDestination(file, context):
    # return (context["recipe_dir"] + "/" + file, context["package_dir_src"] + "/" + file)

# def makeATestContextFrom(context):
    # nc = context.copy()
    # nc["package_name"] = context["package_name"] + "_tests"
    # nc["package_dir"] = context["package_dir"] + "/tests"
    # nc["package_dir"] =  nc["package_dir"] + "/src"
    # nc["cmake_template"] = "TestCMakeLists.txt.tpl"
    # return nc


if __name__ == "__main__":
    import sys
    import runpy
    import os
    if len(sys.argv) != 4:
        print("Usage: mc.py <recipe> <srcpath> <dstpath>")
    print("MasterChief is now cooking '" + sys.argv[1] + "' for you.")
    context = {"from_root" : sys.argv[2] , "to_root": sys.argv[3] }

    if not os.path.exists(context["to_root"]):
        os.makedirs(context["to_root"])

    l=runpy.run_path(sys.argv[1], context)
    sr.runRefactoring(l["command"])
    print("")
