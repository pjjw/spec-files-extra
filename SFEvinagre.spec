#
# spec file for package SFEvinagre
#
# includes module(s): vinagre
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use vinagre = vinagre.spec

Name:               SFEvinagre
Summary:            Vinagre - A VCN client for the GNOME Desktop
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWgnome-base-libs
Requires:           SUNWgnome-libs
Requires:           SUNWgnutls
Requires:           SUNWlibgcrypt
Requires:           SUNWlibgpg-error
Requires:           SUNWavahi-bridge-dsd
Requires:           SUNWlxml
Requires:           SUNWgnome-vfs
Requires:           SUNWgnome-config
Requires:           SUNWgnome-component
Requires:           SUNWxwrtl
Requires:           SUNWlibm
Requires:           SUNWmlib
Requires:           SUNWfontconfig
Requires:           SUNWxorg-clientlibs
Requires:           SUNWdbus
Requires:           SUNWopenssl-libraries
Requires:           SUNWxwplt
Requires:           SUNWfreetype2
Requires:           SUNWlexpt
Requires:           SUNWpng
Requires:           SFEgtk-vnc
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWgnome-libs-devel
BuildRequires:      SUNWgnutls-devel
BuildRequires:      SUNWlibgcrypt-devel
BuildRequires:      SUNWlibgpg-error-devel
BuildRequires:      SUNWavahi-bridge-dsd-devel
BuildRequires:      SUNWlxml-devel
BuildRequires:      SUNWgnome-vfs-devel
BuildRequires:      SUNWgnome-config-devel
BuildRequires:      SUNWgnome-component-devel
BuildRequires:      SUNWmlibh
BuildRequires:      SUNWdbus-devel
BuildRequires:      SUNWpng-devel
BuildRequires:      SFEgtk-vnc-devel

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
%vinagre.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%vinagre.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%vinagre.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/vinagre
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vinagre
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/mimetypes
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%dir %attr (-, root, other) %{_datadir}/doc
%{_datadir}/doc/vinagre
%ghost %attr (-, root, root) %{_datadir}/mime

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Nov 30 2007 - nonsea@users.sourceforge.net
- Initial spec
