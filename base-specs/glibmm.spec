#
# spec file for package glibmm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: simonzheng
#
%include Solaris.inc

Name:                    glibmm
License:        	 LGPL
Group:                   System/Libraries
Version:                 2.14.2
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 glibmm - C++ Wrapper for the Glib2 Library
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.14/%{name}-%{version}.tar.bz2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           libsigc++-devel >= 2.0.0
BuildRequires:           glib2-devel >= 2.9.0

%package devel
Summary:                 Headers for developing programs that will use %{name}.
Group:                   System/Libraries
Requires:                libsigc++-devel >= 1.2.0
Requires:                glib2-devel >= 2.9.0

%prep
%setup -q -n glibmm-%version

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

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/glibmm*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jau 28 2008 - simon.zheng@sun.com
- Create. Split from SFEglibmm and bump to version 2.14.2.
