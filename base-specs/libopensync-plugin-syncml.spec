#
# spec file for package libopensync-plugin-syncml
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
# bugdb: http://www.opensync.org/ticket/
#

Name:           libopensync-plugin-syncml
License:        GPL
Group:          System/Libraries
Version:        0.37
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary:        A plugin allows OpenSync to be synchronized against SyncML capable devices
Source:         http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:	libopensync-devel >= 0.20
BuildRequires:  libsyncml-devel >= 0.4.2

%description
A plugin allows OpenSync to be synchronized against SyncML capable devices. The plugin supports the protocol version 1.0,1.1 and 1.2. Available transports are http and obex.

%package	devel
Summary:        Header files from %name
Group:          Development/C

%description 	devel
Header files for developing programs based on %name.

%prep
%setup -q -n  %{name}-%{version}

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

%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug ../
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ../
%endif


make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
cd build
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*

%files devel
%defattr(-,root,root)
%{_includedir}/opensync-1.0/opensync/*

%changelog
* Thu Spe 04 2008 - halton.huo@sun.com
- Bump to 0.37
* Thu Dec 20 2007 - jijun.yu@sun.com
- Bump to 0.35, change the build tool to cmake.
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.33, change Source to full URL.
- Use scons build
- Remove patch forte-wall.diff
* Tue Apr  3 2007 - laca@sun.com
- enable obex support
* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22. Change source tarball to bz2.
* Thu Jan 11 2007 - jijun.yu@sun.com
- Initial version

