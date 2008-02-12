#
# spec file for package SFElcab.spec
#
# includes module(s): lcab
#
%include Solaris.inc

%define src_name	lcab
%define src_version 1.0b12
%define src_url	    http://www.mirrorservice.org/sites/ftp.freebsd.org/pub/FreeBSD/distfiles

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg:	SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	${src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:                   SFElcab
Summary:                lcab - Microsoft cabinet file creator
Version:                %{src_version}
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}-%{version}
autoreconf
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} 
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

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

