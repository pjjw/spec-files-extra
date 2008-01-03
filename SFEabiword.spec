#
# spec file for package SFEabiword
#
# includes module(s): abiword
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define SUNWaspell      %(/usr/bin/pkginfo -q SUNWaspell && echo 1 || echo 0)

%use abiword = abiword.spec

Name:               SFEabiword
Summary:            %abiword.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:           SUNWuiu8
Requires:           SUNWzlib
Requires:           SUNWgnome-base-libs
Requires:           SUNWpng
Requires:           SUNWlxml
Requires:           SUNWlibpopt
Requires:           SUNWgnome-spell
Requires:           SUNWgnome-character-map
Requires:           SUNWgnome-print
Requires:           SUNWfontconfig
Requires:           SUNWperl584core
Requires:           SFElibfribidi
Requires:           SFElibgsf
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWpng-devel
BuildRequires:      SUNWlxml-devel
BuildRequires:      SUNWlibpopt-devel
BuildRequires:      SUNWgnome-spell-devel
BuildRequires:      SUNWgnome-character-map-devel
BuildRequires:      SUNWgnome-print-devel
BuildRequires:      SFElibfribidi-devel
BuildRequires:      SFElibgsf-devel
%if %SUNWaspell
Requires:           SUNWaspell
BuildRequires:      SUNWaspell-devel
%else
BuildRequires: SFEaspell-devel
Requires: SFEaspell
%endif
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif


%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}


%prep
rm -rf %name-%version
mkdir -p %name-%version
%abiword.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%abiword.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%abiword.install -d %name-%version
#mkdir -p $RPM_BUILD_ROOT%{_bindir}
#cp $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/* $RPM_BUILD_ROOT%{_bindir}/
#rm -rf $RPM_BUILD_ROOT%{_prefix}/X11R6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/abiword*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/icons
%{_datadir}/icons/*.png
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWaspell or SFEaspell. Also add support for
  building on Indiana systems.
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Initial spec
