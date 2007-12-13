#
# spec file for package conduit
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:           conduit
License:        GPL
Group:          System/GUI/GNOME
Version:        0.3.4
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.conduit-project.org/
Summary:        Synchronization for GNOME
Source:         http://files.conduit-project.org/releases/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  dbus-devel >= 0.93
BuildRequires:  pkgconfig
BuildRequires:  python >= 1:2.4
BuildRequires:  python-dateutil
BuildRequires:  python-pygoocanvas >= 0.8.0
BuildRequires:  python-pygtk-devel >= 2:2.10
BuildRequires:  python-vobject
BuildRequires:  rpm-pythonprov
BuildRequires:  rpmbuild(macros) >= 1.219
Requires:       pydoc
Requires:       python-PyXML
Requires:       python-dateutil
Requires:       python-evolution >= 0.0.3
Requires:       python-gdata
Requires:       python-pygoocanvas >= 0.8.0
Requires:       python-pygtk-gtk >= 2:2.10
Requires:       python-vobject

%description
Conduit is a synchronization solution for GNOME which allows the user
to take their emails, files, bookmarks, and any other type of personal
information and synchronize that data with another computer, an online
service, or even another electronic device.

Conduit manages the synchronization and conversion of data into other
formats. For example, conduit allows you to;
 - Synchronize your tomboy notes to a file on a remote computer
 - Synchronize your emails to your mobile phone
 - Synchronize your bookmarks to delicious, gmail, or even your own
   webserver

%package devel
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

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

#intltoolize --force --automake
#libtoolize --force
#aclocal $ACLOCAL_FLAGS -I .
#autoheader
#automake -a -c -f
#autoconf

./configure --prefix=%{_prefix} \
			--bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--libdir=%{_libdir} \
			--datadir=%{_datadir} \
			--includedir=%{_includedir} \
			--sysconfdir=%{_sysconfdir} \

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
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/conduit
%{_bindir}/conduit-client
%{_bindir}/conduit.real
%dir %{_libdir}/conduit
%{_libdir}/conduit/dataproviders
%{_datadir}/applications/conduit.desktop
%dir %{_datadir}/conduit
%{_datadir}/conduit/*.png
%{_datadir}/conduit/*.glade
%{_datadir}/dbus-1/services/*.service
%{_datadir}/gnome/autostart/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/omf/conduit/conduit-C.omf
%dir %{_libdir}/python2.4/site-packages/conduit/conduit
%{_libdir}/python2.4/site-packages/conduit/*.py[co]
%dir %{_libdir}/python2.4/site-packages/conduit/datatypes
%{_libdir}/python2.4/site-packages/conduit/datatypes/*.py[co]
%{_datadir}/gtk-doc/html/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial version