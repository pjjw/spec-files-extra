# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	proj4
%define src_version	4.5.0
%define deploy_name	proj
%define deploy_version	%{src_version}
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	PROJ.4 - Cartographic Projections Library
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	MIT License
Source:         ftp://ftp.remotesensing.org/proj/%{deploy_name}-%{version}.tar.gz
URL:            http://proj.maptools.org
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{deploy_name}-%{version}-build

#Requires:      
#BuildRequires: 

%description 
PROJ.4 is a Cartographic Projections Library. It is in use by many mapping & GIS apps such as GRASS GIS, MapServer, PostGIS, Thuban, OGDI, OGRCoordinateTransformation.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{deploy_name}-%{version}
./configure --prefix=%{_prefix}

#%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_libdir}
%{_libdir}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%dir %attr (0755, root, sys) %{_prefix}/man
%{_prefix}/man/*


%changelog
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
