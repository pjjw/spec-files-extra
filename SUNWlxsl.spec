#
# spec file for package SUNWlxsl
#
# includes module(s): libxslt
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define libxslt_version 1.1.14
%define python_version 2.4

Name:                    SUNWlxsl
Summary:                 The XSLT library
Version:                 11.10.%{libxslt_version}
Source:                  ftp://ftp.gnome.org/pub/GNOME/stable/sources/libxslt/libxslt-%{libxslt_version}.tar.bz2
SUNW_BaseDir:            %{_prefix}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlxml

%package python
Summary:                 Python bindings for libxslt
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SUNWlxml
Requires: SUNWPython

%prep
%setup -c -q -n libxslt-%{libxslt_version}

%ifarch amd64 sparcv9
cp -rp libxslt-%libxslt_version libxslt-%{libxslt_version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%_ldflags"
%ifarch amd64 sparcv9
cd libxslt-%{libxslt_version}-64

export CFLAGS="%optflags64"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH=%{_libdir}/%{_arch64}/pkgconfig
libtoolize --force
aclocal
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir}/%{_arch64} \
				    --libdir=%{_libdir}/%{_arch64} \
				    --bindir=%{_bindir}/%{_arch64} \
                                    --includedir=%{_includedir} \
                                    --without-python \
                                    --mandir=%{_mandir}
make -j$CPUS
cd ..
%endif

cd libxslt-%{libxslt_version}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH=%{_pkg_config_path}
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
cd libxslt-%{libxslt_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/xsltConf.sh
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
cd ..
%endif

cd libxslt-%libxslt_version
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/xsltConf.sh
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rm -rf $RPM_BUILD_ROOT%{_libdir}/python*/*/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/xslt*
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
* Tue Sep 27 2005 - laca@sun.com
- move python bits from site-packages to vendor-packages
* Tue Sep 20 2005 - laca@sun.com
- define SUNWlxsl-python
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Wed Jul 06 2005 - laca@sun.com
- resurrected from the metropolis branch
- moved back to /usr
* Mon Jun 21 2004 - shirley.woos@sun.com
- Changed Requires SUNWlxml to SUNWgnome-xml
* Mon Jun 21 2004 - laca@sun.com
- set PATH and PKG_CONFIG_PATH so that libxslt finds the private copy of
  libxml2
- move libxslt to /usr/lib/jds-private just like libxml2
- rename to SUNWgnome-xslt so we can have 2 copies on the same system

* Mon Mar 22 2004 - laszlo.peter@sun.com
- update to 1.1.4

* Mon Mar 01 2004 - laszlo.peter@sun.com
- initial version based on SuSE's libxslt.spec
