#
# spec file for package tracker
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:           tracker
License:        GPL
Group:          Applications/System
Version:        0.6.4
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.tracker-project.org
Summary:        Desktop search tool
Source:         http://www.gnome.org/~jamiemcc/tracker/tracker-%{version}.tar.bz2

Patch1:         %{name}-01-w3m-crash.diff
Patch2:         %{name}-02-disable-autostart.diff
Patch3:         %{name}-03-r1071-latest.diff
Patch4:         %{name}-04-preferences-explicit-apply.diff
Patch5:         %{name}-05-evo-reload.diff
Patch6:         %{name}-06-thunderbird.diff
Patch7:         %{name}-07-firefox-history.diff
Patch8:         %{name}-08-check-remote.diff
Patch9:         %{name}-09-man.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: gmime-devel, poppler-devel, gettext
BuildRequires: gnome-desktop-devel, gamin-devel
BuildRequires: libexif-devel, libgsf-devel, gstreamer-devel
BuildRequires: desktop-file-utils, intltool
BuildRequires: sqlite-devel
BuildRequires: dbus-devel, dbus-glib


%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database, search tool and indexer.

It consists of a common object database that allows entities to have an
almost infinte number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

It has the ability to index, store, harvest metadata. retrieve and search
all types of files and other first class objects

%package devel
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the static libraries and header files needed for
developing with tracker

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p0
%patch8 -p1
%patch9 -p0

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

intltoolize --force --automake
libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
			--bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--libdir=%{_libdir} \
			--datadir=%{_datadir} \
			--includedir=%{_includedir} \
			--sysconfdir=%{_sysconfdir} \
			--disable-warnings \
			--enable-external-sqlite \

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/htmless
%{_bindir}/o3totxt
%{_bindir}/tracker*
%{_datadir}/tracker/
%{_datadir}/pixmaps/tracker/
%{_datadir}/dbus-1/services/tracker.service
%{_libdir}/*.so.*
%{_mandir}/man1/tracker*.1.gz
%{_sysconfdir}/xdg/autostart/trackerd.desktop

%files devel
%defattr(-, root, root)
%{_includedir}/tracker*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jan 22 2008 - nonsea@users.sourceforge.net
- Add patch preferences-explicit-apply.diff
- Add patch evo-reload.diff
- Add patch man.diff
- Rename r1071-r1092.diff to r1071-latest.diff
- Reorder patches.
* Thu Jan 03 2008 - nonsea@users.sourceforge.net
- Add patch disable-autostart.diff
- Add patch check-remote.diff
- Add patch r1071-r1092.diff
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Unbump to 0.6.3 and remove obsolete patch, 02-thunderbird.
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Initial version, spilit from SFEtracker.spec
