#
# spec file for package SFExtail.spec
#
# includes module(s): xtail

%include Solaris.inc

%define src_name	xtail
%define src_url		http://www.unicom.com/sw/xtail
%define src_version	2.1
%define pkg_release	1

SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFExtail
Summary:                xtail - Watch the growth of files and directories
Version:                2.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir}

%build
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0755 xtail $RPM_BUILD_ROOT%{_bindir}/xtail
install -m 0644 xtail.1 $RPM_BUILD_ROOT%{_mandir}/man1/xtail.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%changelog
* Sun Oct 14 2007 - laca@sun.com
- fix _datadir permissions
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

