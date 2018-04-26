#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os
import json
import re
import shutil
import spm
import inspect
from Cheetah.Template import Template

# sofa-pck-manager add Sofa.Helper.Types

# Move the files (to git)
# git mv

# Add  the files to the package
# sofa-pck-manager package Sofa.Helper.Types add src/*

# Build the CMakeLists
# sofa-pck-manager package Sofa.Helper.Types generate-cmakelists

template = """
#ifndef $INCLUDE_GUARD
#define $INCLUDE_GUARD

// The content of this file has been refactored and moved to this new location
// The best practice is now to update your code. By updating the including points
// as well as the namespace
$INCLUDE_PATH_FORWARD

$NS_FORWARD

#endif // $INCLUDE_GUARD
"""

templateConfig = """
#encoding utf-8
#compiler-settings
commentStartToken = //
directiveStartToken = %
cheetahVarStartToken = autopack::
#end compiler-settings

#ifndef autopack::INCLUDE_GUARD
#define autopack::INCLUDE_GUARD

#include <sofa/config/sharedlibrary_defines.h>

#ifdef BUILD_TARGET_autopack::CNAME
    #define SofaTarget
    #define autopack::{CNAME}_API SOFA_EXPORT_DYNAMIC_LIBRARY
#else
    #define autopack::{CNAME}_API SOFA_IMPORT_DYNAMIC_LIBRARY
#endif

#endif // autopack::INCLUDE_GUARD
"""


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
    
    # spm.addToProperty(package_name, targetname, configfile)

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


def decodeArgs(options, args, context):
    print("CC: " + str(context))
    print("OP: " + str(options))
    print("XX: " + str(args))
    i = 0
    kwargs = {}
    for o in options:
        if o in context:
             kwargs[o] = context[o]
        else:
            print("ARGS: [" + str(args) + "]")
            if i < len(args):
                kwargs[o] = args[i]
                i += 1
            else:
                kwargs[0] = None
    return (args[i:], kwargs)


def spmCmd(command=None, *args, **kwargs):
    if command == "add-to-property":
        spm.addToProperty(*args, **kwargs)
    elif command == "set-property":
        spm.setProperty(*args, **kwargs)
    elif command == "init":
        spm.initPackage(**kwargs)
    elif command == "generate-cmakelists":
        spm.generateCMakeLists(**kwargs)
    elif command == "generate-configfiles":
        spm.generateConfigFiles(**kwargs)
    elif command == "generate-deprecatedlayout":
        spm.generateDeprecatedLayout(**kwargs)
    else:
        print("Invalid spm cmd:" +str(command))


def replacetextCmd(root_dir, str_src, str_dst, **kwargs):
    if os.path.isdir(root_dir):
        for (rootpath, dirname, filenames) in os.walk(root_dir):
            for filename in filenames:
                path = rootpath + "/" + filename
                tmp = open(path + "_tmp","w")
                ## Usefull but we don't have feedback on the repacements done tmp.write(open(path, "r").read().replace(str_src, str_dst))
                for line in open(path, "r"):
                    iline = re.sub(str_src, str_dst, line)
                    if iline != line:
                        print(" - fix " + path + ": " + iline),
                    tmp.write(iline)
                tmp.close()
                shutil.copyfile(path + "_tmp", path)
                os.remove(path + "_tmp")
    else:
        path = root_dir
        tmp = open(path + "_tmp","w")
        for line in open(path, "r"):
            iline = re.sub(str_src, str_dst, line)
            if iline != line:
                print(" - fix " + path + ": " + iline),
            tmp.write(iline)
        tmp.close()
        shutil.copyfile(path + "_tmp", path)
        os.remove(path + "_tmp")


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


def moveCodeAndPatch(filenames, fromFileToFile, forward=None, **kwargs):
    if isinstance(filenames, str):
        filenames = [filename]

    tasks = []

    extToCmakeProperty = {".h" : "header_files", ".inl" : "header_files", ".cpp" : "source_files" }

    for filename in filenames:
        # ext = os.path.splitext(filename)[1]
        srcfilename,dstfilename = fromFileToFile(filename, kwargs)
        for srcfile in glob.glob(srcfilename + ".*"):
            ext = os.path.splitext(srcfile)[1]
            dstfile = dstfilename + ext
            r = os.path.commonprefix([dstfile + "/", kwargs["package_dir_src"] + "/"])
            dstrelativefilename = dstfile[len(r):]
            
            tasks.append(["move", srcfile, dstfile])
            # tasks.append(["rm", srcfile])
            tasks.append(["spm", "add-to-property", extToCmakeProperty[ext], dstrelativefilename, kwargs])

    return tasks


def reorderCommands(tasks):
    mkdir = []
    move = []
    create = []
    spm = []
    fix = []
    last = []
    pre = []
    for i in tasks:
        if i[0] in ["mkdir"]:
            mkdir.append(i)
        elif i[0] in ["move", "rm"]:
            move.append(i)
        elif i[0] in ["mkconfig"]:
            create.append(i)
        elif i[0] in ["spm", "mkforward", "fixheaders"]:
            spm.append(i)
        elif i[0] in ["rename"]:
            fix.append(i)
        elif i[0] in ["post"]:
            last.append(i[1:])
        elif i[0] in ["post"]:
            pre.append(i[1:])
        else:
            last.append(i)
    return pre + mkdir + move + spm + create + fix + last


def execute(cmd, *args, **kwargs):
    if cmd == "replacetext":
        replacetextCmd(*args, **kwargs)
    elif cmd == "move":
        moveCmd(*args, **kwargs)
    elif cmd == "rm":
        rmCmd(*args, **kwargs)
    elif cmd == "mkdir":
        mkdirCmd(*args, **kwargs)
    elif cmd == "spm":
        spmCmd(*args, **kwargs)
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
