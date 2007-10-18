# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	libnjb
%define src_version	2.2.5
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	C library and API for communicating with creative and other audio players
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	BSD license
Group:          Library
Source:         http://nchc.dl.sourceforge.net/sourceforge/libnjb/%{src_name}-%{version}.tar.gz
Patch:        	libnjb-01-2.2.5-p1-makefilechanges.diff
Vendor:       	John Mechalas
URL:            http://libnjb.sourceforge.net
Packager:     	Anil Gulecha
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build



%description 
libnjb is a C library and API for communicating with the Creative Nomad JukeBox
 and Dell DJ digital audio players under BSD, Linux, Mac OS X and Windows. 
 

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
export ac_cv_func_malloc_0_nonnull=yes
export CPPFLAGS=-I/usr/sfw/include
export LDFLAGS=-L/usr/sfw/lib
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

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*


%changelog
* 2007.Aug.11 - Anil
- Initial spec.

