#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os
import json
import re
import shutil
import inspect
from Cheetah.Template import Template
import generator


def runRefactoring(actions):
    if isinstance(actions, str):
        actions = json.loads( open(filename).read() )

    commands = actions["commands"]
    for cmd in commands:
        command = cmd[0]
        args = []
        context = {}

        if len(cmd) != 1:
            if isinstance(cmd[-1], dict):
                args = cmd[1:-1]
                context = cmd[-1]
            else:
                args = cmd[1:]

        args = expand(args, context)

        print(repr(command) + " " + repr(args))

        execute(command, *args, **context)


def moveCodeAndPatch(filenames, fromFileToFile, forward=None, **kwargs):
    if isinstance(filenames, str):
        filenames = [filename]

    tasks = []

    extToCmakeProperty = {".h" : "header_files", ".inl" : "header_files", ".cpp" : "source_files" }
    extToCmakeProperty_test = {".h" : "test_header_files", ".inl" : "test_header_files", ".cpp" : "test_source_files" }

    for filename in filenames:
        # ext = os.path.splitext(filename)[1]
        srcfilename,dstfilename = fromFileToFile(filename, kwargs)
        for srcfile in glob.glob(srcfilename + ".*"):
            ext = os.path.splitext(srcfile)[1]
            dstfile = dstfilename + ext
            if dstfilename.startswith(kwargs["package_dir_src"]):
                r = os.path.commonprefix([dstfile + "/", kwargs["package_dir"] + "/"])
            elif dstfilename.startswith(kwargs["test_package_dir"]):
                r = os.path.commonprefix([dstfile + "/", kwargs["test_package_dir"] + "/"])
            dstrelativefilename = dstfile[len(r):]
            
            tasks.append(["move", srcfile, dstfile])
            # tasks.append(["rm", srcfile])
            if dstfilename.startswith(kwargs["package_dir_src"]):
                tasks.append(["generator", "add-to-property", extToCmakeProperty[ext], dstrelativefilename, kwargs])
            elif dstfilename.startswith(kwargs["test_package_dir"]):
                tasks.append(["generator", "add-to-property", extToCmakeProperty_test[ext], dstrelativefilename, kwargs])
        
        deprecated_prefix = kwargs["package_dir_deprecated"].replace(kwargs["package_dir"] + "/", "")
        tasks.append(["generator", "add-to-property", "deprecated_header_files", deprecated_prefix + "/" + filename + ".h", kwargs])
    return tasks

    
def patchNamespace(base_dir, **kwargs):
    tasks = []
    old_namespace_opening = 'namespace[\t ]+' + '[\n\r\t{ ]*namespace[\t ]+'.join(kwargs["old_namespace"]) + '[\n\r\t ]*{'
    new_namespace_opening = 'namespace ' + '\n{\nnamespace '.join(kwargs["new_namespace"]) + '\n{'
    old_namespace_closing = '}[\t ]*//[\t ]*namespace[\t ]+' + '[\n\r]*}[\t ]*//[\t ]*namespace[\t ]+'.join(reversed(kwargs["old_namespace"]))
    new_namespace_closing = '} // namespace ' + '\n} // namespace '.join(reversed(kwargs["new_namespace"]))
    tasks += [["replacetext", base_dir, old_namespace_opening, new_namespace_opening, kwargs]]
    tasks += [["replacetext", base_dir, old_namespace_closing, new_namespace_closing, kwargs]]
    return tasks
    

def reorderCommands(tasks):
    mkdirCmds = []
    moveCmds = []
    createCmds = []
    generatorCmds = []
    fixCmds = []
    lastCmds = []
    preCmds = []
    for i in tasks:
        if i[0] in ["mkdir"]:
            mkdirCmds.append(i)
        elif i[0] in ["move", "rm"]:
            moveCmds.append(i)
        elif i[0] in ["mkconfig"]:
            createCmds.append(i)
        elif i[0] in ["generator", "mkforward", "fixheaders"]:
            generatorCmds.append(i)
        elif i[0] in ["rename"]:
            fixCmds.append(i)
        elif i[0] in ["post"]:
            lastCmds.append(i[1:])
        elif i[0] in ["post"]:
            preCmds.append(i[1:])
        else:
            lastCmds.append(i)
    return preCmds + mkdirCmds + moveCmds + generatorCmds + createCmds + fixCmds + lastCmds


def execute(cmd, *args, **kwargs):
    if cmd == "replacetext":
        replacetextCmd(*args, **kwargs)
    elif cmd == "move":
        moveCmd(*args, **kwargs)
    elif cmd == "rm":
        rmCmd(*args, **kwargs)
    elif cmd == "mkdir":
        mkdirCmd(*args, **kwargs)
    elif cmd == "generator":
        generatorCmd(*args, **kwargs)
    elif cmd == "commit":
        commitCmd(*args, **kwargs)
    elif cmd == "branch":
        branchCmd(*args, **kwargs)
    elif cmd == "fixheader":
        fixheaderCmd(*args, **kwargs)
    elif cmd == "mkforward":
        forwardCmd(*args, **kwargs)
    elif cmd == "mkconfig":
        mkconfigCmd(*args, **kwargs)
    else:
        print("Invalid command: " + str(cmd))


def generatorCmd(command=None, *args, **kwargs):
    if command == "add-to-property":
        generator.addToProperty(*args, **kwargs)
    elif command == "set-property":
        generator.setProperty(*args, **kwargs)
    elif command == "init":
        generator.initPackage(**kwargs)
    elif command == "generate-cmakelists":
        generator.generateCMakeLists(**kwargs)
    elif command == "generate-cmakelists-tests":
        generator.generateCMakeListsTests(**kwargs)
    elif command == "generate-configfiles":
        generator.generateConfigFiles(**kwargs)
    elif command == "generate-deprecatedlayout":
        generator.generateDeprecatedLayout(**kwargs)
    else:
        print("Invalid generator cmd:" +str(command))


def expand(l, context):
    if isinstance(l, str):
        return str(Template(l, searchList=[context]))
    elif isinstance(l, list):
        nargs = []
        for a in l:
            nargs.append(expand(a,context))
        return nargs
    elif isinstance(l, dict):
        nargs = {}
        for k in l:
            nargs[expand(k, context)] = expand(l[k],context)
        return nargs
    return l


def toCName(p):
    return p.upper().replace("/","_").replace(".","_")


def toCNS(p):
    ns = ""
    for k in p:
        v = p[k]
        if isinstance(v, dict):
            ns += "namespace " + k+" \n"
            ns += "{\n"
            ns += toCNS(v)
            ns += "} // namespace " + k+"\n"
        else:
            ns += "    " + k + v + "\n"
    return ns


def mkconfigCmd(cmd):
    print(" - config: " + str(cmd))
    package_name = cmd[0]
    targetname = "header_files"
    configfile = cmd[1]
    config_template_cmake = TEMPLATES_DIR + "/config/" + "config.template.cmake.in"
    config_template_h = TEMPLATES_DIR + "/config/" + "config.template.h"
    config_template_cpp = TEMPLATES_DIR + "/config/" + "config.template.cpp"
    
    # generator.addToProperty(package_name, targetname, configfile)

    theFile = open(package_name + "/" + configfile, "w")
    templateMap = {
        "INCLUDE_GUARD" : toCName(package_name + "_" + targetname + "_H"),
        "CNAME" : toCName(package_name)
    }
    t = Template(open(template_location).read(), searchList=[templateMap])
    theFile.write(str(t))


def forwardCmd(cmd):
    print(" - forwarding: " + str(cmd))
    package_name = cmd[0]
    finalpath = package_name + "/deprecated_layout/"
    oldpath=cmd[1]
    newpath=cmd[2]
    nsmap=cmd[3]

    if not os.path.exists(finalpath):
        os.mkdir(finalpath)

    theFile = open(finalpath + "/" + oldpath, "w")
    templateMap = {
        "INCLUDE_GUARD" : toCName(oldpath),
        "INCLUDE_PATH_FORWARD" : "#include <" + newpath + ">",
        "NS_FORWARD" : toCNS(nsmap)
    }
    t = Template(template, searchList=[templateMap])
    theFile.write(str(t))


def branchCmd(cmd):
    print(" - branch: git" + str(cmd))


def mkdirCmd(dirname, **kwargs):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    # print(" - make dir " + dirname)


def commitCmd(cmd):
    print(" - commit: git" + str(cmd))


def moveCmd(sourcefile, destfile, **kwargs):
    # print(" - move: " + str(sourcefile))
    shutil.copy(sourcefile, destfile)


def rmCmd(path, **kwargs):
    try:
        os.remove(path)
    except OSError:
        os.rmdir(path)


def fixheaderCmd(cmd):
    print(" - fixheader: " + str(cmd))
    path = cmd[0]
    tmp = open(path + "_tmp","w")

    for line in open(path, "r"):
        iline = re.sub(cmd[1], cmd[2], line)
        if iline != line:
            print("- fix " + path + ": " + iline),
        tmp.write(iline)
    tmp.close()
    shutil.copyfile(path + "_tmp", path)
    os.remove(path + "_tmp")


def replacetextCmd(root_dir, str_src, str_dst, **kwargs):
    if os.path.isdir(root_dir):
        for (rootpath, dirname, filenames) in os.walk(root_dir):
            for filename in filenames:
                path = rootpath + "/" + filename
                replaceTextInFile(path, str_src, str_dst)
    else:
        path = root_dir
        replaceTextInFile(path, str_src, str_dst)

        
def replaceTextInFile(filename, str_src, str_dst):
    file = open(filename, "r")
    text = file.read() # Read the file and assigns the value to a variable
    file.close() # Close the file (read session)    
    file = open(filename, "w")
    file.write( re.sub(str_src, str_dst, text) )
    file.close() # Close the file (write session)
