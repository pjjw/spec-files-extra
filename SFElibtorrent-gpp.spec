#
# spec file for package SFElibtorrent-gpp
#
# includes module(s): libtorrent
#
%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/sfw/bin/g++
%include base.inc

%use libtorrent = libtorrent.spec

Name:		SFElibtorrent-gpp
Summary:	%{libtorrent.summary}
Version:	%{libtorrent.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFEsigcpp-gpp-devel
Requires:  SFEsigcpp-gpp

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%libtorrent.prep -d %name-%version/%{base_arch}

%build
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%libtorrent.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%libtorrent.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*

%changelog
* Fri May  9 2008 - laca@sun.com
- Initial version
