#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, os
from Cheetah.Template import Template
import mc
from mc import moveCodeAndPatch, reorder, nameMap

context = {
    "package_name" : "Sofa.Type",
    "package_dir" : rootdstdir+"/Sofa.Type",
    "dstdir" : rootdstdir+"/Sofa.Type/src/",
    "recipedir" : os.path.dirname(__file__),
    "oldheaders" : ["SOFA_HELPER"]
}

tasks = []

tasks += [["spm", "init", context]]
#tasks += [["spm", "add-to-property", "dependencies", ["Sofa.Config", "Sofa.Messaging"], context]]
tasks += [["mkdir", "${package_dir}/src/mc/test", context]]
tasks += moveCodeAndPatch(["mylib.cpp", "mylib.h"], nameMap, **context)

tasks += [["spm", "generate-cmakelists", context]]
command = {"commands" : tasks}
#command = {"commands" : reorder(tasks)}
   


