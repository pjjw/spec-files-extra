#
# spec file for package vinagre
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:           vinagre
License:        GPL
Group:          Development/Libraries
Version:        2.24.1
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.gnome.org/projects/vinagre
Summary:        A VCN client for the GNOME Desktop
Source:         http://download.gnome.org/sources/%{name}/2.24/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel

%description
vinagre is  a VCN client for the GNOME Desktop

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
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
%{_libdir}/bonobo/servers/GNOME_RemoteDesktop.server

%changelog
* Tue Sep 09 2008 - halton.huo@sun.com
- Bump to 2.23.92
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 2.23.91
- Remove upstreamed patch libsocket.diff
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 2.23.90
- Add patch libsocket.diff to fix bugzilla #548585
* Tue Mar 10 2008 - nonsea@users.sourceforge.net
- Bump to 0.5.0
* Tue Mar 04 2008 - nonsea@users.sourceforge.net
- Bump to 0.4.92
- Remove upstreamed patch gthread.diff
* Wed Feb 20 2008 - nonsea@users.sourceforge.net
- Bump to 0.4.91
- Remove upstreamed patch wall.diff
- Add new patch gthread.diff to fix bugzilla #517603.
* Thu Dec 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.4
- Add patch wall.diff to fix build problem on Solaris.
* Fri Nov 30 2007 - nonsea@users.sourceforge.net
- Initial version
