#encoding utf-8
#compiler-settings
commentStartToken = ///
directiveStartToken = %
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
#ifndef SOFA_${file_cname}_DEPRECATEDLAYOUT_H
#define SOFA_${file_cname}_DEPRECATEDLAYOUT_H

#include <${file_include}>

%set $complete_new_namespace = '::'.join($new_namespace)
%set $step_old_namespace = ''
%for $namespace in $old_namespace
namespace $namespace
{
%if $step_old_namespace
%set $step_old_namespace = $step_old_namespace + "::" + $namespace
%else
%set $step_old_namespace = $namespace
%end if
%end for

// Auto-generated "using" based on old_namespace and new_namespace
// See recipe for details
using $complete_new_namespace::$component

// You can also set some $step_old_namespace::* alias here
// Example: to make the old namespace $step_old_namespace::something point to the new $complete_new_namespace
// namespace something = $complete_new_namespace

%for $namespace in reversed($old_namespace)
} // namespace $namespace
%end for

#endif // SOFA_${file_cname}_DEPRECATEDLAYOUT_H
