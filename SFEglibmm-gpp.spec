#
# spec file for package SFEglibmm-gpp
#
# includes module(s): glibmm
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use glibmm = glibmm.spec

Name:                    SFEglibmm-gpp
Summary:                 glibmm - C++ Wrapper for the Glib2 Library (g++-built)
Version:                 %{glibmm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWsigcpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%glibmm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
%glibmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%glibmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/m4
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/pm
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/libglibmm_generate_extra_defs*.so*
rm -rf $RPM_BUILD_ROOT%{_cxx_includedir}/glibmm-2.4/glibmm_generate_extra_defs

# REMOVE l10n FILES - included in Solaris
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# remove files included in SUNWglibmm-devel:
rm -r $RPM_BUILD_ROOT%{_datadir}
rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%{_cxx_libdir}/glibmm*

%changelog
* Thu Mar 27 2008 - simon.zheng@sun.com
- Add SUNWglibmm.copyright.
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version number.
* Fri 29 2008 - simon.zheng@sun.com
- Pack devhelp index file. 
* Wed Feb 15 2008 - simon.zheng@sun.com
- Pack file /usr/lib/giomm-2.4/giommconfig.h.
* Thu Feb 14 2008 - simon.zheng@sun.com
- Remove useless m4, pm and extra_gen_defs files.
* Mon Jau 28 2008 - simon.zheng@sun.com
- Split into SUNWglibmm.spec and glibmm.spec.
- Change download URL to GNOME official website.
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.12.10
* Tue Apr 17 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.8.
* Fri Mar 16 2007 - laca@sun.com
- bump to 2.12.7
* Wed Jan 03 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.4
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEglibmm
- update permissions
- bump to 2.10.4
* Fri May 12 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Fri Mar 10 2006 - damien.carbery@sun.com
- Bump to 2.10.0.
* Thu Nov 17 2005 - laca@sun.com
- create
