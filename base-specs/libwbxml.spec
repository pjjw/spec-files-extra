#
# spec file for package SFEwbxml
#
# includes module(s): wbxml2
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
# bugdb: http://libwbxml.opensync.org/ticket/
#

Summary:	WBXML parser and compiler library
Name:		libwbxml
Version:	0.10.1
Release:	1
License:	LGPL
Group:		Development/Libraries
Distribution:   Java Desktop System
Vendor:		Sun Microsystems, Inc.
URL:		http://libwbxml.opensync.org/
Source:		http://%{sf_mirror}/%{name}/%{name}-%{version}.tar.bz2
# date:2009-01-08 type:bug owner:halton bugid:25
Patch1:		%{name}-01-getopt.diff

BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/doc
Requires:	expat >= 1.95.4
BuildRequires:	expat-devel >= 1.95.4
AutoReqProv:	yes
Provides:	wbxml2

%description
wbxml2 is a library that includes a WBXML parser and a WBXML compiler.
Unlike wbxml, it does not depend on libxml2 but on expat, making it faster and more portable.

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

mkdir build && cd build
%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug -DENABLE_INSTALL_DOC=False ..
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DENABLE_INSTALL_DOC=False ..
%endif

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
cd build
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-,root,root)
%doc AUTHORS bootstrap BUGS ChangeLog COPYING GNU-LGPL INSTALL NEWS README References THANKS TODO doxygen.h
%attr(755,root,root) %{_bindir}/*

%changelog 
* Thu Jan 08 2009 - halton.huo@sun.com
- Bump to 0.10.1
- Rename to libwbxml
- Change to use cmake
- Add patch getopt to fix bug #25
* Thu Jan 11 2007 - jijun.yu@sun.com
- Initial version
