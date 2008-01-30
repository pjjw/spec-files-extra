#
# spec file for package libopensync-plugin-gcal
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jeryyu
#

%define real_name libopensync-plugin-google-calendar

Name:           libopensync-plugin-gcal
License:        GPL
Group:          System/Libraries
Version:        0.36
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary:        Google calendar plugin for opensync synchronization tool
Source:         http://www.opensync.org/download/releases/%{version}/%{real_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:	libopensync-devel >= 0.30

%description
This plugin allows applications using OpenSync to synchronise to and from
Google Calendar.

%package	devel
Summary:        Header files from %name
Group:          Development/C

%description 	devel
Header files for developing programs based on %name.

%prep
%setup -q -n  %{real_name}-%{version}

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

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ../

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
cd build
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*

%changelog
* Wed Jan 30 2008 - jijun.yu@sun.com
- Bump to 0.36.
* Thu Dec 20 2007 - jijun.yu@sun.com
- Bump to 0.35, change the build tool to cmake.
* Wed Oct 17 2007 - laca@sun.com
- disable parallel build
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.33, change Source to full URL.
* Tue Aug 07 2007 - jijun.yu@sun.com
- Bump to 0.32.
* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22. Change source tarball to bz2.
* Tue Nov 14 2006 - halton.huo@sun.com
- Initial version

