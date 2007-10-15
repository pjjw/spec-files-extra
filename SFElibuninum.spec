#
# spec file for package SFElibuninum.spec
#
# includes module(s): libuninum
#
%include Solaris.inc

%define src_name	libuninum
%define src_url	    http://billposer.org/Software/Downloads
%define src_version	2.5
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFElibuninum
Summary:                libuninum - A Library for converting Unicode strings to numbers and numbers to Unicode strings
Version:                2.5
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms
Requires: SFEgmp
BuildRequires: SFEgmp-devel

%prep
%setup -q -n %{src_name}-%{version}
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

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%dir %attr(0755,root,bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Oct 14 2007 - laca@sun.com
- fix _datadir permissions
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

