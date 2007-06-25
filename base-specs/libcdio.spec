#
# spec file for package libcdio
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:         libcdio
License:      LGPL
Group:        System Environment/Libraries
Version:      0.78.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Utilities for CD interaction
Source:       http://ftp.gnu.org/gnu/libcdio/%{name}-%{version}.tar.gz
URL:          http://ftp.gnu.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
Utilities for CD interaction

%package devel
Summary: Headers for developing programs that will use libcdio
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use libcdio.

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
automake -a -c -f
autoconf
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--disable-cpp-progs --disable-cxx
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so

%changelog
* Mon Jun 23 2007 - irene.huang@sun.com
- created.
