#
# spec file for package SFEtre.spec
#
# includes module(s): TRE
#
%include Solaris.inc

%define src_name	tre
%define src_url		http://laurikari.net/tre
%define src_version	0.7.5
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFEtre
Summary:                TRE - Lightweight, Robust, and Efficient POSIX compliant regexp matching library 
Version:                0.7.5
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir}

%build
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%dir %attr(0755,root,bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

