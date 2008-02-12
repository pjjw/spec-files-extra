#
# spec file for package SFEmsort.spec
#
# includes module(s): msort
#
%include Solaris.inc

%define src_name	msort
%define src_url	    	http://dl.exactcode.de/t2/source/7.0/m
%define src_version	8.40
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFEmsort
Summary:                msort - A program for sorting files in sophisticated ways
Version:                8.40
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms
Requires: SFElibuninum
Requires: SFEgmp
Requires: SFEtre
Requires: SFEutf8proc
BuildRequires: SUNWgcc
BuildRequires: SFElibuninum

%prep
%setup -q -n %{src_name}-%{version}
export CC=gcc
export CXX=g++
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} \
            --disable-allocaok
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


%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

