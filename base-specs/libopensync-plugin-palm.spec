#
# spec file for package libopensync-plugin-palm
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:           libopensync-plugin-palm
License:        GPL
Group:          System/Libraries
Version:        0.35
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary:        Palm plugin for OpenSync
Source:         http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

Requires:       libpilot-link
Requires:       libopensync = %version
BuildRequires: libopensync-devel = %version

%description
This plugin allows applications using OpenSync to synchronise to and from
Palm based devices.

%package devel
Summary: Header files, libraries and development documentation for %name
Group: System/Libraries
Requires: %name = %version

%description devel
This package contains the header files, static libraries and development
documentation for %name. If you like to develop programs using %name,
you will need to install %name-devel.


%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
  %define plink_prefix /usr/sfw
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ../

make -j $CPUS

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
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%_libdir/opensync/plugins/*.so
%_libdir/opensync/formats/*.so
%_datadir/opensync/defaults/*

%files devel
%_includedir/opensync-1.0/opensync/*.h


%changelog
* Thu Dec 20 2007 - jijun.yu@sun.com
- Bump to 0.35, change the build tool to cmake.

* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.33, change Source to full URL.
- Remove patch forte-wall.diff
- Add patch detect-plink.diff and nouse-headers.diff

* Mon Aug 06 2007 - jijun.yu@sun.com
- Bump to 0.32.

* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22. Change source tarball to bz2.

* Fri Nov 17 2006 - halton.huo@sun.com
- Initial version
