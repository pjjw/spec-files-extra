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

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root

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
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/vinagre/[a-z][a-z]
rm $RPM_BUILD_ROOT%{_datadir}/omf/vinagre/vinagre-[a-z][a-z].omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post root
%include gconf-install.script

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x $PKG_INSTALL_ROOT/usr/bin/gconftool-2 || {';
  echo '  echo "WARNING: gconftool-2 not found; not uninstalling gconf schemas"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$BASEDIR/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$BASEDIR%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/vinagre.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas > /dev/null'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS_wait -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/vinagre
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vinagre-applet
%dir %attr (0755, root, bin) %{_libdir}/bonobo
%dir %attr (0755, root, bin) %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/GNOME_VinagreApplet.server
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vinagre
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/mimetypes
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/vinagre/C
%{_datadir}/omf/vinagre/vinagre-C.omf
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%dir %attr (-, root, other) %{_datadir}/doc
%{_datadir}/doc/vinagre
%dir %attr (-, root, root) %{_datadir}/mime
%dir %attr (-, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/vinagre-mime.xml
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/omf/vinagre/vinagre-[a-z][a-z].omf
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/vinagre/[a-z][a-z]
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/vinagre.schemas


%changelog
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Update %files becuase verion upgrading
* Wed Feb 20 2008 - nonsea@users.sourceforge.net
- Add -root package, add %post and %preun -root package.
- Update files according updated version.
* Fri Nov 30 2007 - nonsea@users.sourceforge.net
- Initial spec
