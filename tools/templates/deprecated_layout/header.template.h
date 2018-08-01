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

%set $step_old_namespace = ''
%set $old_namespace_copy = list($old_namespace)
%set $last_old_namespace = $old_namespace_copy.pop()
%set $complete_new_namespace = '::'.join($new_namespace)
%for $namespace in $old_namespace_copy
namespace $namespace
{
%if $step_old_namespace
%set $step_old_namespace = $step_old_namespace + "::" + $namespace
%else
%set $step_old_namespace = $namespace
%end if
%end for

// Namespace forwarding: solution 1
// Auto-generated alias to make $step_old_namespace::$last_old_namespace point to $complete_new_namespace
// namespace $last_old_namespace = $complete_new_namespace;

// Namespace forwarding: solution 2
// Auto-generated "using" Component
// This solution looks clearer but could miss other classes declared in ${component}.h
namespace $last_old_namespace
{
using $complete_new_namespace::$component;
} // namespace $last_old_namespace

%for $namespace in reversed($old_namespace_copy)
} // namespace $namespace
%end for

#endif // SOFA_${file_cname}_DEPRECATEDLAYOUT_H
