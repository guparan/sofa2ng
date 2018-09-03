#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import shutil
import fnmatch
import re
from Cheetah.Template import Template

TEMPLATES_DIR = os.path.dirname(__file__) + "/templates"

emptypackage = {
        "package_name" : "undefined",
        "package_type" : "undefined",
        "dependencies" : [],
        "header_files" : [],
        "source_files" : [],
        "extra_files" : []
}


def toLine(l):
    s=""
    for i in l:
        s += " " + i
    return s


def generateCMakeLists(package_name, package_dir=None, cmake_template="CMakeLists.template.cmake", **kwargs):
    if package_dir == None:
        package_dir = package_name
    print("   - generating " + package_dir + "/CMakeLists.txt")

    theFile = open(package_dir + "/CMakeLists.txt", "w + ")
    dependency_targets = getDependencyTargets(kwargs["dependencies"], kwargs["from_root"])
    setProperty("dependency_targets", dependency_targets, package_name, package_dir=package_dir)
    context = loadPackage(package_name, package_dir=package_dir)

    templatebasepath = os.path.dirname(os.path.abspath(__file__)) + "/templates"
    templatelocation = templatebasepath + "/" + cmake_template
    if os.path.exists(cmake_template):
        templatelocation = cmake_template
    elif os.path.exists(templatelocation):
        pass
    else:
        print(" - failed to find a valid template in")
        print("   search for: " + cmake_template)
        print("   search for: " + templatelocation)
        return

    if not os.path.exists(templatelocation):
        print(" - failed to find a valid template in " + templatelocation)
        return

    t = Template( open(templatelocation).read(), searchList=[context, {"cmake_template_src_path" : templatelocation}])
    theFile.write(str(t))


def generateCMakeListsTests(package_name, package_dir=None, cmake_template="tests/CMakeLists.template.cmake", **kwargs):
    print("PACKAGE_DIR = " + package_dir)
    # package_dir = context["test_package_dir"]
    # context["sorted_test_dependencies"] = toLine( context["test_dependencies"] )
    setProperty("test_dependency_targets", kwargs["test_dependencies"], package_name, package_dir=package_dir)
    context = loadPackage(package_name, package_dir)

    print("   - generating " + package_dir + "/tests/CMakeLists.txt")

    theFile = open(package_dir + "/tests/CMakeLists.txt", "w + ")

    templatebasepath = os.path.dirname(os.path.abspath(__file__)) + "/templates"
    templatelocation = templatebasepath + "/" + cmake_template
    if os.path.exists(cmake_template):
        templatelocation = cmake_template
    elif os.path.exists(templatelocation):
        pass
    else:
        print(" - failed to find a valid template in")
        print("   search for: " + cmake_template)
        print("   search for: " + templatelocation)
        return

    if not os.path.exists(templatelocation):
        print(" - failed to find a valid template in " + templatelocation)
        return

    t = Template( open(templatelocation).read(), searchList=[context, {"cmake_template_src_path" : templatelocation}])
    theFile.write(str(t))
    
    # if os.path.isdir(package_dir + "/tests"):
    #     if not os.path.isdir(package_dir + "/tests/.generator"):
    #         shutil.copytree(package_dir + "/.generator", package_dir + "/tests/.generator")
    #     
    #     print("kwargs = ")
    #     for x in kwargs:
    #         if isinstance(kwargs[x], basestring):
    #             print (x + " : " + kwargs[x])
    #         else:
    #             print (x + " :")
    #             for y in kwargs[x]:
    #                 print ("  - " + y)
    #     generateCMakeLists(package_name, package_dir + "/tests", "tests/CMakeLists.template.cmake", **context)


def generateConfigFiles(package_name, package_dir=None, **kwargs):
    # print("   - generateConfigFiles: " + str(package_name))
    
    config_dir = kwargs["package_dir_config"]
    config_template_cmake = TEMPLATES_DIR + "/config/" + "config.template.cmake.in"
    config_template_h = TEMPLATES_DIR + "/config/" + "config.template.h"
    config_template_cpp = TEMPLATES_DIR + "/config/" + "config.template.cpp"
    
    context = loadPackage(package_name, package_dir=package_dir)
    
    # Generate config/PackageName.cmake.in
    theFile = open(config_dir + "/" + package_name + ".cmake.in", "w+")
    t = Template( open(config_template_cmake).read(), searchList=[context] )
    theFile.write(str(t))
    
    # Generate config/PackageName.h
    theFile = open(config_dir + "/" + package_name + ".h", "w+")
    t = Template( open(config_template_h).read(), searchList=[context] )
    theFile.write(str(t))
    
    # Generate config/PackageName.cpp
    theFile = open(config_dir + "/" + package_name + ".cpp", "w+")
    t = Template( open(config_template_cpp).read(), searchList=[context] )
    theFile.write(str(t))
    
    
def generateDeprecatedLayout(package_name, package_dir=None, **kwargs):
    # print("   - generateDeprecatedLayout: " + str(package_name))
    deprecatedlayout_dir = kwargs["package_dir_deprecated"]
    deprecatedlayout_template = TEMPLATES_DIR + "/deprecated_layout/" + "header.template.h"
    
    context = loadPackage(package_name, package_dir=package_dir)
    
    # fromFiles = kwargs["src_from"] * kwargs["package_components"]
    for component in kwargs["package_components"]:         
        file = component + ".h"
        context["component"] = component
        context["file_include"] = '/'.join(context["new_namespace"]) + '/' + file
        context["file_cname"] = component.upper()
        theFile = open(deprecatedlayout_dir + "/" + file, "w+")
        t = Template( open(deprecatedlayout_template).read(), searchList=[context] )
        theFile.write(str(t))


def getDependencyTargets(dependencies, from_root):
    targets = []
    for (rootpath, dirname, filenames) in os.walk(from_root):
        for filename in fnmatch.filter(filenames, '*CMakeLists.txt'):
            filepath = rootpath + "/" + filename
            for dep in dependencies:
                if not re.search('Sofa[A-Z].*', dep): # not standard Sofa dep
                    targets += dep
                    break # one more target found
                filestring = open(filepath).read()
                if re.search('.*project\( *'+dep+' *\).*', filestring):
                    # print(dep + " is in " + filepath)
                    found = re.search('.*sofa_install_targets\( *([A-Za-z0-9]+).*', filestring)
                    if found:
                        targets += [found.group(1)]
                        break # one more target found
            if len(targets) == len(dependencies):
                break # all targets found
    return list(set(targets)) # unique list of targets


def loadGenerator(generatorfilename):
    return json.loads( open(generatorfilename).read() )


def addPackageGroup(name):
    print("Adding a package group: " + name)


def savePackage(package_name, package, package_dir=None, **kwargs):
    if package_dir == None:
        package_dir = package_name
    generatordir = package_dir + "/" + ".generator"
    generatorfile = generatordir + "/config.json"
    # for k in package:
        # if isinstance( package[k], list ):
            # package[k].sort()
    open(generatorfile, "w").write( json.dumps(package, sort_keys=True, indent=4, separators=(',', ': ')) )


def loadPackage(package_name, package_dir=None, **kwargs):
    if package_dir == None:
        package_dir = package_name
    generatordir = package_dir + "/" + ".generator"
    generatorfile = generatordir + "/config.json"
    if os.path.exists(generatorfile):
        generator = loadGenerator(generatorfile)
        # generator["package_cname"] = generator["package_name"].replace(".","_").upper()
        return generator
    print("unable to load generator file from "  +  package_dir)
    return None


def addToProperty(property_name, property_value, package_name, **kwargs):
    # print("   - adding to property '" + property_name + "' value: " + str(property_value))
    package = loadPackage(package_name, **kwargs)

    if property_name not in package:
        package[property_name] = []

    if isinstance(property_value, list):
        package[property_name] += property_value
    else:
        package[property_name].append(property_value)
    savePackage(package_name, package,**kwargs)


def setProperty(property_name, property_value, package_name, **kwargs):
    # print("   - setting property '" + property_name + "' to package '" + package_name + "'")
    package = loadPackage(package_name, **kwargs)
    package[property_name] = property_value
    savePackage(package_name, package, **kwargs)


def initPackage(package_name, package_dir, package_type="library", **kwargs):
    finalpath = package_dir
    print("   - init package in " + finalpath)
    print("    - name : '" + package_name + "'")
    print("    - path: '" + finalpath + "'")
    parentpath=""
    pathdec = package_name.split('/')
    for p in pathdec[:-1]:
        parentpath += p + "/"
        if os.path.exists(parentpath):
            print("    - path exist:" + parentpath)
        else:
            groupname = parentpath.replace('/', '.')
            print("    - create group: " + groupname)
            #generatordir = parentpath + "/" + ".generator"
            #generatorfile = generatordir + "/config.json"
            os.makedirs(parentpath)
            #os.makedirs(generatordir)
            #open(generatorfile, "w").write( json.dumps( emptypackage ) )
            #setProperty(groupname, "package_name", groupname)
            #setProperty(groupname, "package_type", "group")

    if pathdec[-1]:
        if not os.path.exists(finalpath):
            print("    - create dir")
            os.makedirs(finalpath)
        generatordir = finalpath + "/" + ".generator"
        if not os.path.exists(generatordir):
            print("    - create generator dir")
            os.makedirs(generatordir)
        generatorfile = generatordir + "/config.json"
        print("   - save package description in: " + generatorfile)
        open(generatorfile, "w").write( json.dumps(  emptypackage ) )
        setProperty("package_name", package_name, package_name, package_dir=package_dir)
        setProperty("package_type", package_type, package_name, package_dir=package_dir)
        setProperty("package_cname", package_name.replace(".","_").upper(), package_name, package_dir=package_dir)
        for value in kwargs:
            setProperty(value, kwargs[value], package_name, package_dir=package_dir)

