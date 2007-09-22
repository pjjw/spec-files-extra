#
# spec file for package SFElibutf8proc.spec
#
# includes module(s): libutf8proc
#
%include Solaris.inc

%define src_name	utf8proc
%define src_url		http://www.flexiguided.de/pub
%define src_version	1.1.2
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFElibutf8proc
Summary:                UTF-8 Processing Library
Version:                v1.1.2
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}

%build
make c-library

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT%{_libdir}
install -d -m 0755 $RPM_BUILD_ROOT%{_includedir}
install -m 0755 libutf8proc.a $RPM_BUILD_ROOT%{_libdir}/libutf8proc.a
install -m 0755 utf8proc.h $RPM_BUILD_ROOT%{_includedir}/utf8proc.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755,root,bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

