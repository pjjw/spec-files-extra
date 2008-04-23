#
# spec file for package SFEsigcpp-gpp
#
# includes module(s): libsigc++
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use sigcpp = sigcpp.spec

Name:                    SFEsigcpp-gpp
Summary:                 Libsigc++ - a library that implements typesafe callback system for standard C++ (g++-built)
Version:                 %{sigcpp.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%sigcpp.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%sigcpp.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%sigcpp.install -d %name-%version
rm $RPM_BUILD_ROOT%{_cxx_libdir}/lib*a
# comes with SUNWsigcpp-devel
rm -r $RPM_BUILD_ROOT%{_datadir}
# comes with SUNWsigcpp-devel
rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%{_cxx_libdir}/sigc++*

%changelog
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWsigcpp.spec to build with g++
