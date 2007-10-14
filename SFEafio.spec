#
# spec file for package SFEafio.spec
#
# includes module(s): afio
#
%include Solaris.inc

%define src_name	afio
%define src_url		http://www.ibiblio.org/pub/linux/system/backup/
%define src_version 2.5
# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:                   SFEafio
Summary:                AFIO - An archiving engine capable of cpio compatible output
Version:                %{src_version}
Source:                 %{src_url}/%{src_name}-%{version}.tgz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
URL:                    http://members.brabant.chello.nl/~k.holtman, http://members.chello.nl/~k.holtman
Patch0:                 %{src_name}-01-%{version}.gcc.diff

Requires: SUNWcsl
Requires: SUNWlibms
BuildRequires: SUNWgcc

%prep
%setup -q -n %{src_name}-%{version}
%patch0 -p1

%build
CC=gcc CXX=g++ make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/man1/*

%changelog
* Sat Oct 13 2007 - laca@sun.com
- fix _datadir permissions
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

