#
# spec file for package SFEgnome-power-manager
#
# includes module(s): gnome-power-manager
#
%include Solaris.inc
%use gpm = gnome-power-manager.spec

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)
%define with_libnotify %(pkginfo -q SUNWlibnotify && echo 1 || echo 0)

Name:                    SFEgnome-power-manager
Summary:                 GNOME Power Manager
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgnome-base-libs
BuildRequires:           SUNWgnome-base-libs-devel
Requires:                SUNWgnome-libs
BuildRequires:           SUNWgnome-libs-devel
Requires:                SUNWdbus
BuildRequires:           SUNWdbus-devel
Requires:                SUNWdbus-bindings
BuildRequires:           SUNWdbus-bindings-devel
%if %with_hal
Requires:                SUNWhal
%endif
Requires:                SUNWdbus-bindings
%if %with_libnotify
Requires:                SUNWlibnotify
BuildRequires:           SUNWlibnotify-devel
%endif
Requires:                SUNWgnome-panel
BuildRequires:           SUNWgnome-panel-devel
Requires:                SUNWpostrun

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gpm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export LDFLAGS="%_ldflags -lX11"
%gpm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gpm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Delete scrollkeeper files
rm -rf $RPM_BUILD_ROOT/var


%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '_usr/bin/gconftool-2 --makefile-install-rule $SDIR/gnome-power-manager.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%preun root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '_usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/gnome-power-manager.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/bonobo
%dir %attr (0755, root, bin) %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/GNOME_BrightnessApplet.server
%{_libdir}/bonobo/servers/GNOME_InhibitApplet.server
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/autostart
%{_datadir}/gnome/autostart/gnome-power-manager.desktop
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%dir %attr (0755, root, bin) %{_datadir}/gnome/help/gnome-power-manager
%{_datadir}/gnome/help/gnome-power-manager/*/*
%dir %attr (0755, root, bin) %{_datadir}/gnome-2.0
%dir %attr (0755, root, bin) %{_datadir}/gnome-2.0/ui
%{_datadir}/gnome-2.0/ui/GNOME_BrightnessApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_InhibitApplet.xml
%dir %attr (0755, root, bin) %{_datadir}/gnome-power-manager
%{_datadir}/gnome-power-manager/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/gnome-power-manager.service
%dir %attr (0755, root, bin) %{_datadir}/omf/
%dir %attr (0755, root, bin) %{_datadir}/omf/gnome-power-manager
%{_datadir}/omf/gnome-power-manager/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gnome-power-*.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1


%files root
%defattr (0755, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-power-manager.schemas
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/gnome-power-manager.conf

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Mar 28 2007 - simon.zheng@sun.com
- Create