#
# spec file for package SFEgtk-vnc
#
# includes module(s): gtk-vnc
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use gvnc = gtk-vnc.spec

Name:               SFEgtk-vnc
Summary:            gvnc.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWgnome-base-libs
Requires:           SUNWgnome-libs
Requires:           SUNWgnome-python-libs
Requires:           SUNWgnutls
Requires:           SUNWlibgcrypt
Requires:           SUNWlibgpg-error
Requires:           SUNWzlib
Requires:           SUNWxwrtl
Requires:           SUNWxwplt
Requires:           SUNWmlib
Requires:           SUNWlibm
Requires:           SUNWfontconfig
Requires:           SUNWfreetype2
Requires:           SUNWxorg-clientlibs
Requires:           SUNWpng
Requires:           SUNWlexpt
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWgnome-libs-devel
BuildRequires:      SUNWgnome-python-libs-devel
BuildRequires:      SUNWgnutls-devel
BuildRequires:      SUNWlibgcrypt-devel
BuildRequires:      SUNWlibgpg-error-devel
BuildRequires:      SUNWmlibh
BuildRequires:      SUNWpng-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

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
%gvnc.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%gvnc.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gvnc.install -d %name-%version
rmdir $RPM_BUILD_ROOT%{_bindir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/python*
%dir %attr (0755, root, bin) %{_libdir}/python*/site-packages
%{_libdir}/python*/site-packages/gtkvnc.so

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue May 06 2008 - nonsea@users.sourceforge.net
- Remove ast stuff.
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Initial spec
