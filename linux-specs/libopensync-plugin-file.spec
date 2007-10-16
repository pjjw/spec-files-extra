#
# spec file for package libopensync-plugin-file
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
#


Name:           libopensync-plugin-file
License:        GPL
Group:          System/Libraries
Version:        0.33
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary:        File plugin for opensync synchronization tool
Source:         http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
Patch1:         %{name}-01-forte-wall.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:	opensync-devel >= %{version}
BuildRequires:	fam-devel

%description
This plugin allows applications using OpenSync to synchronise to and from
files stored on disk.

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
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*


%changelog
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.33, change Source to full URL.

* Mon Aug 06 2007 - jijun.yu@sun.com
- Bump to 0.32

* Mon Jul 09 2007 - nonsea@users.sourceforge.net
- Bump to 0.31.

* Wed Jun 05 2007 - jijun.yu@sun.com
- Bump to 0.30.

* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Bump to 0.22. Change source tarball to bz2.

* Tue Nov 28 2006 - harry.lu@sun.com
- Add patch libopensync-plugin-file-02-null-crash.diff

* Fri Nov 17 2006 - halton.huo@sun.com
- Initial version
