#
# spec file for package SFEgoffice
#
# includes module(s): goffice
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use goffice = goffice.spec

Name:                    SFEgoffice
Summary:                 goffice - Document centric set of APIs
Version:                 %{goffice.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWlxml
Requires:       SUNWzlib
Requires:       SUNWlibgsf
Requires:       SUNWlibms
Requires:       SUNWgnome-libs
Requires:       SUNWgnome-base-libs
Requires:       SUNWgnome-python-libs
BuildRequires:  SUNWlxml-devel
BuildRequires:  SUNWgnome-libs-devel
BuildRequires:  SUNWgnome-base-libs-devel
BuildRequires:  SUNWgnome-python-libs-devel
%if %option_with_gnu_iconv
Requires:       SUNWgnu-libiconv
Requires:       SUNWgnu-gettext
%else
Requires:       SUNWuiu8
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
BuildRequires: SUNWgnome-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%goffice.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%goffice.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%goffice.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgoffice*.so*
%{_libdir}/goffice
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/goffice
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Split base part to base/goffice.spec
- Bump to 0.6.4
* Mon Apr 14 2008 - trisk@acm.jhu.edu
- Bump to 0.6.2, update dependencies
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
