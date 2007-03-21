#
# spec file for package SFEwbxml
#
# includes module(s): wbxml2
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%include Solaris.inc

%use wbxml2 = wbxml2.spec

Name:               SFEwbxml
Summary:            wbxml2 - WBXML parser and compiler library 
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%wbxml2.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export RPM_OPT_FLAGS="$CFLAGS"
%wbxml2.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%wbxml2.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libwbxml2*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Add devel package and correct file permissions.

* Thu Jan 11 2007 - jijun.yu@sun.com 
- initial version created
