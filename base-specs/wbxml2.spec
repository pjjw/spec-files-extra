#
# spec file for package SFEwbxml
#
# includes module(s): wbxml2
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%define name	wbxml2
%define ver	0.9.2
%define RELEASE	1
%define rel	%{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}
%define prefix	/usr

Summary:	WBXML parser and compiler library
Name:		%name
Version:	%ver
Release:	%rel
License:	LGPL
Group:		Development/Libraries
Distribution:   Java Desktop System
Vendor:		Sun Microsystems, Inc.
URL:		http://libwbxml.aymerick.com/

Source:		http://prdownloads.sourceforge.net/wbxmllib/%{name}-%{ver}.tar.gz
Patch1:		%{name}-01-Makefile.diff
Patch2:		%{name}-02-getopt.diff

BuildRoot:	%{_tmppath}/%{name}-%{ver}-build
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
%patch2 -p1

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
export CFLAGS="$CFLAGS -I/usr/sfw/include"
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
            --mandir=%{_mandir}                 \

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
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
* Thu Jan 11 2007 - jijun.yu@sun.com
- Initial version
