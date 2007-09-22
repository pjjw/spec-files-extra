# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	medit
%define src_version	0.8.9
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Preamble 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Text editor
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Group:          Development/Tools
Source:         http://jaist.dl.sourceforge.net/sourceforge/mooedit/%{src_name}-%{src_version}.tar.bz2
Patch:		    medit-01-0.8.9-solaris.sunstudio12.diff
Vendor:       	medit
URL:            http://mooedit.sourceforge.net
Packager:     	Komala, Jayanthi
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
#BuildRoot:     %{_builddir}/%{name}-root

%description 
GNU auotool

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q
CC=gcc
export CC
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir}

%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications
%{_datadir}/icons
%{_datadir}/moo
%{_datadir}/man
%{_datadir}/mime
%{_datadir}/pixmaps
%{_datadir}/locale
%{_basedir}/lib
%{_basedir}/include


%changelog
* By Komala, Jayanthi
- Initial spec
