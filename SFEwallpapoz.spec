# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	wallpapoz
%define src_version	0.4
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	/usr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Wallpapoz -- Gnome Desktop Wallpapers Configuration Tool
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Source:         http://wallpapoz.akbarhome.com/files/%{src_name}-%{version}.tar.bz2
Vendor:       	Akbar
URL:            http://wallpapoz.akbarhome.com
Packager:     	Shivakumar GN
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build

Requires:     SUNWgnome-python-desktop  SUNWgnome-python-libs SUNWpython-imaging
#BuildRequires:

%description 

Wallpapoz enables automatic changing of Gnome desktop wallpapers based on timer, workspace.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_basedir}
python setup.py install --installdir $RPM_BUILD_ROOT/%{_basedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
%{_datadir}/gnome/help/%{src_name}
%{_datadir}/applications/%{src_name}.desktop
%{_datadir}/pixmaps/%{src_name}.png
%{_datadir}/locale/*


%changelog
* 2008.April.15 - <shivakumar dot gn at gmail dot com>
- Initial spec.
