# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	gnomad2
%define src_version	2.8.13
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Gnomad2 is a GTK+ music manager for Creative Zen
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2 license
Group:          Multimedia/Audio Manager
Source:         http://jaist.dl.sourceforge.net/sourceforge/gnomad2/%{src_name}-%{version}.tar.gz
Requires: 	SFElibnjb
Requires:	SFElibid3tag
Requires:   SFElibnjb
BuildRequires:	SFElibid3tag-devel

Patch:        	gnomad2-01-2.8.13_p1_LDADD.diff
Vendor:       	Linus Walleij
URL:            http://gnomad2.sourceforge.net
Packager:     	Anil Gulecha, Indraneel RR
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build

%description 
Gnomad2 is a GTK+ music manager and swiss army knife for the Creative Labs NOMAD
and Zen range plus the Dell DJ devices using the Portable Digital Entertainment (PDE) protocol. 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix}

%patch0 -p 1

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* 2007.Aug.11 - Anil Gulecha, Indraneel RR
- Initial spec.
