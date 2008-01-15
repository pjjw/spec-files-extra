#
# spec file for package vinagre
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#


Name:           vinagre
License:        GPL
Group:          Development/Libraries
Version:        0.4
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.gnome.org/projects/vinagre
Summary:        A VCN client for the GNOME Desktop
Source:         http://download.gnome.org/sources/%{name}/0.4/%{name}-%{version}.tar.bz2
# date:2007-12-13 bugzilla:503358 owner:halton type:bug
Patch1:         %{name}-01-wall.diff
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel

%description
vinagre is  a VCN client for the GNOME Desktop

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

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-avahi=yes
	

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
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%{_bindir}/*
%{_libdir}/lib*.so.*

%changelog
* Thu Dec 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.4
- Add patch wall.diff to fix build problem on Solaris.
* Fri Nov 30 2007 - nonsea@users.sourceforge.net
- Initial version
