#
# spec file for package msynctool
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
#

Name:           msynctool
License:        GPL
Group:          Applications
Version:        0.36
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary:        OpenSync data synchronization command line programs
Source:	        http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2

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

%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr
%endif

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
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
* Wed Jan 30 2008 - jijun.yu@sun.com
- Bump to 0.36.

* Thu Dec 20 2007 - jijun.yu@sun.com
- Bump to 0.35.

* Mon Nov 05 2007 - jijun.yu@sun.com
- Bump to 0.34.
- Change to cmake build tool.

* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.33, change Source to full URL.

* Mon Aug 06 2007 - jijun.yu@sun.com
- Bump to 0.32.

* Thu Jul 12 2007 - jijun.yu@sun.com
- Disable enable_rpath at configuring and remove msynctool-02-ld-rpath.diff

* Tue Jul 10 2007 - nonsea@users.sourceforge.net
- Bump to 0.31.
- Add patch msynctool-02-ld-rpath.diff to fix ld issue.

* Fri Jun 05 2007 - jijun.yu@sun.com
- Bump to 0.30

* Mon Apr 02 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22.

* Tue Nov 14 2006 - halton.huo@sun.com
- Initial version

