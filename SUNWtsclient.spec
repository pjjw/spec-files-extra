#
# spec file for package SUNWtsclient
#
# includes module(s): tsclient
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use tsclient = tsclient.spec

Name:               SUNWtsclient
Summary:            tsclient - A frontend for rdesktop for the GNOME2 platform.
Version:            %{tsclient.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWgnome-panel
Requires:           SUNWgnome-libs
Requires:           SUNWxwplt
Requires:           SUNWxwice
Requires:           SUNWgnome-vfs
Requires:           SUNWgnome-config
Requires:           SUNWgnome-base-libs
Requires:           SUNWlibpopt
Requires:           SUNWlibm
Requires:           SUNWmlib
Requires:           SUNWfontconfig
Requires:           SUNWxorg-clientlibs
Requires:           SUNWgnome-component
Requires:           SUNWlxml
Requires:           SUNWdbus-bindings
Requires:           SUNWdbus
Requires:           SUNWopenssl-libraries
Requires:           SUNWgnome-audio
Requires:           SUNWfreetype2
Requires:           SUNWlexpt
Requires:           SUNWzlib
Requires:           SUNWpng
BuildRequires:      SUNWgnome-panel-devel
BuildRequires:      SUNWgnome-libs-devel
BuildRequires:      SUNWgnome-vfs-devel
BuildRequires:      SUNWgnome-config-devel
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWlibpopt-devel
BuildRequires:      SUNWmlibh
BuildRequires:      SUNWgnome-component-devel
BuildRequires:      SUNWlxml-devel
BuildRequires:      SUNWdbus-bindings-devel
BuildRequires:      SUNWdbus-devel
BuildRequires:      SUNWsfwhea
BuildRequires:      SUNWgnome-audio-devel
BuildRequires:      SUNWpng-devel

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
%tsclient.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%tsclient.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%tsclient.install -d %name-%version

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
%{_bindir}/tsclient
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tsclient-applet
%dir %attr (0755, root, bin) %{_libdir}/bonobo
%dir %attr (0755, root, bin) %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/GNOME_TSClientApplet.server
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/tsclient.applications
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/tsclient.desktop
%dir %attr (-, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%dir %attr (-, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Jan 19 2008 - nonsea@users.sourceforge.net
- Initial spec
