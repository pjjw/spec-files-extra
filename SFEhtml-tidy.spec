# ===========================================================================
#                    Spec File for Html Tidy
# ===========================================================================
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%define src_name	tidy
%define src_version	051026
%define pkg_release	1

%define deploy_prefix	/usr/local


# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg:	SFE%{src_name}
SUNW_ProdVers:	${src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	HTML parser and pretty printer
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	W3C license
Group:          Application/Web
Source:	        http://tidy.sourceforge.net/src/old/%{src_name}_src_%{src_version}.tgz
Patch:        	tidy-01-051026.diff
Vendor:       	Dave Raggett
URL:            http://tidy.sourceforge.net
Packager:     	Ravi,Saurabh
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build


#Ideally these should be included for requires: glib2, gtk2, pango
#Requires:      
#BuildRequires: 

%description 
HTML Tidy is an open source program and library for checking and generating clean XHTML/HTML.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}

%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
cd build/gmake
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
cd build/gmake
make install DESTDIR=$RPM_BUILD_ROOT

echo "_prefix  %{_prefix}"
echo "RPM   $RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)

%dir %attr (0755, root, bin)  %{deploy_prefix}/bin
%{deploy_prefix}/bin/*
%dir %attr (0755, root, bin) %{deploy_prefix}/lib
%{deploy_prefix}/lib/*
%dir %attr (0755, root, bin) %{deploy_prefix}/include
%{deploy_prefix}/include/*

%changelog
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Remove architecture from package name.
* 2007.06.25 - Ravibharadwaj & Saurabh vyas
- Initial spec
