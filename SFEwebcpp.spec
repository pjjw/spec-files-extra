#
# spec file for package SFEwebcpp.spec
#
# includes module(s): Webcpp
#
%include Solaris.inc

%define src_name	webcpp
%define src_url		http://heanet.dl.sourceforge.net/sourceforge/webcpp
%define src_version	0.8.4
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}


Name:                   SFEwebcpp
Summary:                Webcpp - Webcpp converts source code into syntax highlighted HTML
Version:                0.8.4
Source:                 %{src_url}/%{src_name}-%{version}-src.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}-%{version}-src
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --datadir=%{_datadir}

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

%dir %attr(0755,root,bin) %{_datadir}
%dir %attr(0755,root,bin) %{_datadir}/webcpp
%{_datadir}/webcpp/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

