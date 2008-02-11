# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	boost
%define src_version	1_34_1
%define deploy_version	1.34.1
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg:       SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{deploy_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Boost library for static compilation (source only)
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	Boost Software License
Group:          Developement
Source:         %{sf_download}/boost/%{src_name}_%{version}.tar.bz2
#Patch:        	yourpatch-name
Vendor:       	http://www.boost.org
URL:            http://www.boost.org
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

#Requires:      
#BuildRequires: 

%description 
Boost library for static compilation (source only)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep
%setup -q -n %{src_name}_%{version}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
echo "boost library does not need a build..."

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
#Using install command is technically more appropriate
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{src_name}-%{deploy_version}/
cp -r . $RPM_BUILD_ROOT/%{_prefix}/%{src_name}-%{deploy_version}/
rm -f $RPM_BUILD_ROOT/%{_prefix}/%{src_name}-%{deploy_version}/.pkgbuild.build.sh
rm -f $RPM_BUILD_ROOT/%{_prefix}/%{src_name}-%{deploy_version}/.pkgbuild.install.sh
%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_prefix}/%{src_name}-%{deploy_version}
%{_prefix}/%{src_name}-%{deploy_version}/*


#%dir %attr (0755, root, other) %{_datadir}/applications
#%{_datadir}/applications/*



%changelog
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
