#
# spec file for package SFEpoppler-gpp
#
# includes module(s): poppler
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use poppler = poppler.spec

Name:                    SFEpoppler-gpp
Summary:                 poppler - PDF rendering library (g++-built)
Version:                 %{poppler.version}
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
Requires: SFEsigcpp-gpp-devel
Requires: SUNWsigcpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%poppler.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
%poppler.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%poppler.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# REMOVE l10n FILES - included in Solaris
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# remove files included in SUNWgnome-pdf-viewer[-devel]:
rm -r $RPM_BUILD_ROOT%{_datadir}
rm -r $RPM_BUILD_ROOT%{_includedir}
rm -r $RPM_BUILD_ROOT%{_bindir}

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

%changelog
* Wed Apr 23 2008 - laca@sun.com
- create
