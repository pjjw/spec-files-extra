#
# spec file for package msynctool
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
#

Name:		msynctool
License:	GPL
Group:		Applications
Version:        0.31
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.opensync.org/
Summary:	OpenSync data synchronization command line programs
Source:	        %{name}-%{version}.tar.bz2
Patch1:         %{name}-01-forte-wall.diff
Patch2:         %{name}-02-ld-rpath.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc

%description
OpenSync is a synchronization framework that is platform and distribution
independent.

It consists of several plugins that can be used to connect to devices,
a powerful sync-engine and the framework itself.

This package contains command line program to use OpenSync framework.

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
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

scons prefix=%{_prefix}                 \

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
scons install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Tue Jul 10 2007 - nonsea@users.sourceforge.net
- Bump to 0.31.
- Add patch msynctool-02-ld-rpath.diff to fix ld issue.

* Fri Jun 05 2007 - jijun.yu@sun.com
- Bump to 0.30

* Mon Apr 02 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22.

* Tue Nov 14 2006 - halton.huo@sun.com
- Initial version

