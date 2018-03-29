# sofa2ng

All that is very drafty. Consider it more as proof of concept.

## SPM
spm stand for sofa-package-manage, a tools that combines a
json dictonnary describing a project (stored in a .spm directory)
and a template to generate consistent CMakeLists for sofa. Maybe
one day this tools (like a real packages manager) may automatically
download the sources files from remotes locations and may have a
web site to search into the sofa packages.

## sr
sr stand for sofa-refactor. I'm not sure this tool is really usefull
but it implement a set of common command that are often used while
refactoring Sofa. With sr it is possible to execute a "replay" of
a sequence of code transformation that can be more complex than
just applying a patch to a file as git do (I'm not sure this is not
a bad idea...but until proven it is I will continue to use it).

sr understand only sequence of refactoring command. To avoid repeating
very long list of changes it is recommanded to use helper code that
generate the refactring command from a more factored form of changes written
in python. This factored form of change is called a recipe (the file extension is
.rcpy)

## mc
mc stand for MasterChief...because it can load the recipy (.rcpy) file,
generating a refactoring sequence that is then passed to sr for replay.
