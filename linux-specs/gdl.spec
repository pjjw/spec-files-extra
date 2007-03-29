#
# spec file for package gdl
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:		gdl
License:	GPL
Group:		Development/Libraries
Version:	0.7.3
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.gnome.org
Summary:	Components and library for GNOME development tools.
Source:		http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.7/%{name}-%{version}.tar.bz2
# date:2006-03-28 bugzilla:407393 owner:nonsea type:bug
Patch1:         %{name}-01-void0-suncc-error.diff
# date:2006-03-28 bugzilla:423802 owner:nonsea type:bug
Patch2:         %{name}-02-define-FUNCTION.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

Requires: 	gtk2 >= 2.4.0
Requires: 	libgnomeui >= 2.6.0
Requires: 	libxml2 >= 2.2.8
Requires: 	libglade2 >= 2.0.0

%description
This package contains components and libraries that are intended to be
shared between GNOME development tools, including gnome-build and anjuta2.

The current pieces of GDL include:

# - A code-editing bonbono component based on the Scintilla
#   widget (scintilla-control).
#
Now the editor widget is the glimmer component that use gtksourceview

 - A utility library that also contains the stubs and skels for
   the above components (gdl).


%package devel
Summary:	Libraries and include files for gdl.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and header files if you want to make use of the gdl library in your
own programs.


%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

./configure --prefix=%{_prefix} \
    --bindir=%{_bindir} --mandir=%{_mandir} \
    --localstatedir=%{_localstatedir} --libdir=%{_libdir} \
    --datadir=%{_datadir} --includedir=%{_includedir} \
    --sysconfdir=%{_sysconfdir}

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
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_prefix}/lib/lib*.so.*
%{_prefix}/share/gdl
%{_prefix}/share/locale/*/LC_MESSAGES/*

%files devel
%defattr (-, root, root)
%{_prefix}/include/libgdl-1.0
%{_prefix}/lib/lib*.a
%{_prefix}/lib/lib*.la
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*

%changelog
* Thu Mar 29 2007 nonsea@users.sourceforge.net
- Add patch define-FUNCTION.diff.

* Wed Mar 28 2007 - daymobrew@users.sourceforge.net
- Bump to 0.7.3.

* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
