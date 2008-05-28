#
# spec file for package SFElibtasn1
#
# includes module(s): libtasn1
#
%include Solaris.inc

%define	src_name libtasn1
%use libtasn1 = libtasn1.spec

Name:                SFElibtasn1
Summary:             Tiny ASN.1 library
Version:             %{libtasn1.version}
SUNW_BaseDir:        %{_prefix}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libtasn1.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CXX="$CXX -norunpath"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -staticlib=stlport4"
export MSGFMT="/usr/bin/msgfmt"
%libtasn1.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libtasn1.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
* Wed May 28 2008 - jeff.cai@sun.com
- Split to two spec files
