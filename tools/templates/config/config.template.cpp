#encoding utf-8
#compiler-settings
commentStartToken = ///
directiveStartToken = %
cheetahVarStartToken = autopack::
#end compiler-settings
/******************************************************************************
*       SOFA, Simulation Open-Framework Architecture, development version     *
*                (c) 2006-2018 INRIA, USTL, UJF, CNRS, MGH                    *
*                                                                             *
* This program is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This program is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this program. If not, see <http://www.gnu.org/licenses/>.        *
*******************************************************************************
* Authors: The SOFA Team and external contributors (see Authors.txt)          *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/
#include <autopack::{package_name}.h>

%for autopack::namespace in autopack::new_namespace
namespace autopack::namespace
{
%end for

extern "C" {
    autopack::{package_cname}_API void initExternalModule();
    autopack::{package_cname}_API const char* getModuleName();
    autopack::{package_cname}_API const char* getModuleVersion();
    autopack::{package_cname}_API const char* getModuleLicense();
    autopack::{package_cname}_API const char* getModuleDescription();
    autopack::{package_cname}_API const char* getModuleComponentList();
}

void initExternalModule()
{
    static bool first = true;
    if (first)
    {
        first = false;
    }
}

const char* getModuleName()
{
    return "autopack::package_name";
}

const char* getModuleVersion()
{
    return "1.0";
}

const char* getModuleLicense()
{
    return "LGPL";
}

const char* getModuleDescription()
{
    return getModuleName();
}

const char* getModuleComponentList()
{
    %set autopack::componentlist = ', '.join(autopack::package_components)
    return "autopack::componentlist";
}

%for autopack::namespace in reversed(autopack::new_namespace)
} // namespace autopack::namespace
%end for
