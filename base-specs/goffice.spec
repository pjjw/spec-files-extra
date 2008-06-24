#
# spec file for package goffice
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#


Name:           goffice
Summary:        Set of document centric objects and utilities for glib/gtk
License:        GPL
Group:          System/Libraries
Version:        0.6.4
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.gnome.org/
Source:         http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.6/%{name}-%{version}.tar.gz
# date:2008-06-24 owner:halton type:bug bugzilla:539930
Patch1:         %{name}-01-no-sunmath-lib.diff
BuildRoot:      %{tmpdir}/%{name}-%{version}-root

BuildRequires:  automake1.8
BuildRequires:  intltool
BuildRequires: gtk+2-devel
BuildRequires: libgnomeprint-devel >= 2.8.2
BuildRequires: libgsf-devel >= 1:1.13.3
BuildRequires: libglade2.0-devel
BuildRequires: gtk-doc
BuildRequires: perl-XML-Parser


%description
There are common operations for document centric applications that are
conceptually simple, but complex to implement fully.
    - plugins
    - load/save documents
    - undo/redo

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

aclocal $ACLOCAL_FLAGS
libtoolize --force
intltoolize --force --automake
autoheader
automake -a -f -c --gnu
autoconf

CFLAGS="$RPM_OPT_FLAGS"
./configure  --prefix=%{_prefix}                \
             --libdir=%{_libdir}                \
             --libexecdir=%{_libexecdir}        \
             --datadir=%{_datadir}              \
             --mandir=%{_mandir}                \
             --sysconfdir=%{_sysconfdir}        \
             %gtk_doc_option

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
%doc README NEWS AUTHORS BUGS ChangeLog MAINTAINERS
%{_libdir}/lib*.so*
%dir %{_libdir}/%name/
%{_datadir}/%name
%{_datadir}/pixmaps/%name
%{_includedir}/libgoffice-0.3/
%attr(644,root,root) %{_libdir}/lib*a
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/goffice/


%changelog
* Thu Jan 19 2008 - nonsea@users.sourceforge.net
- Initial version
