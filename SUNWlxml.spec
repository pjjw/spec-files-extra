#
# spec file for package SUNWlxml
#
# includes module(s): libxml2
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define libxml2_version 2.6.23
%define python_version 2.4

Name:                    SUNWlxml
Summary:                 The XML library
Version:                 11.10.%{libxml2_version}
Source:                  http://ftp.gnome.org/pub/gnome/sources/libxml2/2.6/libxml2-%{libxml2_version}.tar.bz2
SUNW_BaseDir:            %{_prefix}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package python
Summary:                 Python bindings for libxml2
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SUNWlxml
Requires: SUNWPython
BuildRequires: SUNWPython-devel

%prep
%setup -c -q -n %name-%version

%ifarch amd64 sparcv9
cp -rp libxml2-%libxml2_version libxml2-%{libxml2_version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%_ldflags"
%ifarch amd64 sparcv9
cd libxml2-%{libxml2_version}-64

export CFLAGS="%optflags64"
export RPM_OPT_FLAGS="$CFLAGS"
libtoolize --force
aclocal
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir} \
				    --libdir=%{_libdir}/%{_arch64} \
				    --bindir=%{_bindir}/%{_arch64} \
                                    --includedir=%{_includedir} \
                                    --without-python \
                                    --mandir=%{_mandir}
make -j$CPUS

cd ..
%endif

cd libxml2-%{libxml2_version}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
libtoolize --force
aclocal
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir} \
				    --libdir=%{_libdir} \
				    --bindir=%{_bindir} \
                                    --includedir=%{_includedir} \
                                    --mandir=%{_mandir}
make -j$CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
%ifarch amd64 sparcv9
cd libxml2-%{libxml2_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/lib*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/xml2Conf.sh
rm -rf $RPM_BUILD_ROOT/%{_bindir}/%{_arch64}
%endif

cd libxml2-%libxml2_version
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

rm -rf $RPM_BUILD_ROOT/%{_datadir}/man
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/xml2Conf.sh
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/vendor-packages/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/xml*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/pkgconfig
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/doc
%{_datadir}/aclocal

%files python
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python*

%changelog
* Thu Dec 08 2005 - damien.carbery@sun.com
- Add BuildRequires SUNWPython-devel. Build fails if python not installed.
* Tue Sep 27 2005 - laca@sun.com
- move python bits from site-packages to vendor-packages
* Tue Sep 20 2005 - laca@sun.com
- define SUNWlxml-python
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Wed Jul 06 2005 - laca@sun.com
- resurrected from the metropolis branch
- moved back to /usr
* Mon Jun 21 2004 - laca@sun.com
- fix %_libdir and %_includedir permissions
- move %_bindir contents to %_libdir/jds-private/bin
* Mon Mar 01 2004 - laszlo.peter@sun.com
- initial version
