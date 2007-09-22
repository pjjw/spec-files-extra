# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	   asterisk
%define src_version    1.4.10.1
%define pkg_release	   1
%define _varetcdir     /var/etc
%define _varlogdir     /var/log
%define _varoptdir     /var/opt
%define _varrundir     /var/run
%define _varspooldir   /var/spool
%define _optdir        /opt
%define _usrincludedir /usr/include

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	/

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Asterisk : Complete IP PBX in software
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPL
Group:          Communication
Source:         http://downloads.digium.com/pub/asterisk/releases/%{src_name}-%{version}.tar.gz
Patch:        	asterisk-01-include.relocate.diff
Vendor:       	http://www.asterisk.org
URL:            http://www.asterisk.org
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

#Requires:      
#BuildRequires: 

%description 
Asterisk is a complete IP PBX in software. It runs on a wide variety of operating systems and provides all of the features one would expect from a PBX including many advanced features that are often associated with high end (and high cost) proprietary PBXs. Asterisk supports Voice over IP in many protocols, and can interoperate with almost all standards-based telephony equipment using relatively inexpensive hardware.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
CC=gcc
CXX=g++
rm -rf ./grep
ln -s /usr/sfw/bin/ggrep ./grep
PATH="`pwd`:$PATH"
echo "`type grep`"
./configure --prefix=%{_prefix}

%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
rm ./grep
ln -s /usr/sfw/bin/ggrep ./grep
PATH="`pwd`:$PATH"
echo "`type grep`"
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)

%dir %attr (0755, root, sys) %{_varoptdir}/%{src_name}
%{_varoptdir}/%{src_name}/*

%dir %attr (0755, root, sys) %{_varetcdir}/%{src_name}

%dir %attr (0755, root, sys) %{_varlogdir}/%{src_name}
%{_varlogdir}/%{src_name}/*

%dir %attr (0755, root, sys) %{_varrundir}/%{src_name}

%dir %attr (0755, root, sys) %{_varspooldir}/%{src_name}
%{_varspooldir}/%{src_name}/*

%dir %attr (0755, root, bin) %{_optdir}/%{src_name}/bin
%dir %attr (0755, root, bin) %{_optdir}/%{src_name}/sbin
%{_optdir}/%{src_name}/sbin/*

%dir %attr (0755, root, sys) %{_optdir}/%{src_name}/include
%{_optdir}/%{src_name}/include/*

%dir %attr (0755, root, sys) %{_optdir}/%{src_name}/lib
%{_optdir}/%{src_name}/lib/*

%dir %attr (0755, root, sys) %{_optdir}/%{src_name}/man
%{_optdir}/%{src_name}/man/*



%changelog
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
