#
# spec file for package libopensync-plugin-syncml
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#owner jerryyu
#

Name: 	 	libopensync-plugin-syncml
License:	GPL
Group:		Office
Version:        0.20
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary: 	A plugin allows OpenSync to be synchronized against SyncML capable devices
Source:		%{name}-%{version}.tar.gz
Patch1: 	%{name}-01-forte-wall.diff
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
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*

%files devel
%defattr(-,root,root)
%{_includedir}/opensync-1.0/opensync/*

%changelog
* Thu Jan 11 2007 - jijun.yu@sun.com
- Initial version

