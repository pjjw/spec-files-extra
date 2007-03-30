#
# spec file for package msynctool
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:		msynctool
License:	GPL
Group:		Applications
Version:        0.22
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.opensync.org/
Summary:	OpenSync data synchronization command line programs
Source:	        %{name}-%{version}.tar.bz2
Patch1:         %{name}-01-forte-wall.diff

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
            --mandir=%{_mandir}                 \

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
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
* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22. Change source tarball to bz2.

* Tue Nov 14 2006 - halton.huo@sun.com
- Initial version

