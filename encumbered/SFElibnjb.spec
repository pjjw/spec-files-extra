# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	libnjb
%define src_version	2.2.6
%define pkg_release	1

# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	C library and API for communicating with creative and other audio players
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	BSD license
Group:          Library
Source:         %{sf_download}/libnjb/%{src_name}-%{version}.tar.gz
Patch:        	libnjb-01-2.2.6-p1-makefilechanges.diff
Vendor:       	John Mechalas
URL:            http://libnjb.sourceforge.net
Packager:     	Anil Gulecha
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build
SUNW_BaseDir:	%{_prefix}

BuildRequires: SFEdoxygen

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
autoreconf --install --force
./configure --prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--disable-static \
	--enable-shared \
	--mandir=%{_mandir}

%patch0 -p1

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Jun 29 2008 - river@wikimedia.org
- BuildRequires: SFEdoxygen
* Fri Jan 25 2008 - moinak.ghosh@sun.com
- Fix one more directory permission.
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Fix directory permissions, enable building shlib, add SUNW_BaseDir
- Re-generate libnjb patch using gdiff
* Sun Dec 30 2007 - markwright@internode.on.net
- Bump to 2.2.6
* 2007.Aug.11 - Anil
- Initial spec.

