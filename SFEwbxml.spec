#
# spec file for package SFEwbxml
#
# includes module(s): libwbxml
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%include Solaris.inc

%use libwbxml = libwbxml.spec

Name:               SFEwbxml
Summary:            libwbxml - WBXML parser and compiler library 
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlexpt
BuildRequires: SUNWcmake
BuildRequires: SFEcheck

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libwbxml.prep -d %name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
%libwbxml.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libwbxml.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Jan 08 2209 - halton.huo@sun.com
- Rename wbxml2 to libwbxml
- Update Requires/BuildRequires after run check_depes.pl
* Mon Mar 17 2008 - sh162551@users.sourceforge.net
- Change the LDFLAGS and CFLAGS since libexpat has
been moved to /usr/lib
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Add devel package and correct file permissions.
* Thu Jan 11 2007 - jijun.yu@sun.com 
- initial version created
