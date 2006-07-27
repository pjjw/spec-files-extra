#
# spec file for package SUNWgnome-img-organizer
#
# includes module(s): gthumb
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use gthumb = gthumb.spec

Name:                    SUNWgnome-img-organizer
Summary:                 GNOME image organizer (gthumb)
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-img-organizer-root
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-camera
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-panel
Requires: SUNWgnome-vfs
Requires: SUNWjpg
Requires: SUNWlibexif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWxwrtl
Requires: SUNWpostrun
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWlibexif-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-file-mgr-devel
BuildRequires: SUNWgnome-camera-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWgnome-base-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

%prep
rm -rf %name-%version
mkdir %name-%version
%gthumb.prep -d %name-%version

%build
export PKG_CONFIG_PATH="%{_pkg_config_path}:/usr/sfw/lib/pkgconfig"
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -lm -L/usr/sfw/lib -R/usr/sfw/lib"

%gthumb.build -d %name-%version

%install
%gthumb.install -d %name-%version

# Delete unneeded scrollkeeper files.
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}(gthumb):$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT/usr/sfw}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/gthumb.schemas'
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
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/gthumb.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/*
%{_libdir}/gthumb/lib*.so*
%{_libdir}/gthumb/modules/lib*.so*
%{_libexecdir}/gthumb-image-viewer
%{_libexecdir}/gthumb-catalog-view
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/gnome-2.0
%{_datadir}/gthumb
%{_datadir}/icons
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gthumb.schemas

%changelog
* Fri Jun  2 2006 - laca@sun.com
- use post/postun scripts to install schemas into the merged gconf files
* Thu May 11 2006 - laca@sun.com
- kill -share pkg, remove eog.1 man page.
* Mon May 01 2006 - damien.carbery@sun.com
- Add %{_datadir}/icons to share package.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Set PKG_CONFIG_PATH to find libgphoto; Set LDFLAGS to link with libpng.
* Sat Jan 28 2006 - damien.carbery@sun.com
- Add BuildRequires for '-devel' equivalents of the Requires packages.
- Added BuildRequires SUNWgnome-camera-devel for gthumb.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Mon Oct 03 2005 - damien.carbery@sun.com
- Remove unpackaged files.
* Sat Dec 18 2004 - damien.carbery@sun.com
- Move gthumb to /usr/sfw per ARC decision.
* Sun Nov 14 2004 - laca@sun.com
- move gthumb to /usr/demo/jds
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Mon Jun 26 2004  shirley.woo@sun.com
- change eog.1 permissions to 0755 for Solaris integration error
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Tue May 18 2004 - laca@sun.com
- add sfw to LDFLAGS/CPPFLAGS (patch from Shirley)
* Tue May 11 2004 - brian.cameron@sun.com
- add %{_datadir}/eog to files share so glade files
  get installed.  This corrects core dumping problem
  when bringing up preferences dialog.
* Tue May 04 2004 - laca@sun.com
- add SUNWgnome-camera dependency
* Fri Mar 26 2004 - laca@sun.com
- add SUNWgnome-file-mgr dependency (for eel)
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Mar 01 2004 - <laca@sun.com>
- fix dependencies
- define PERL5LIB
- file %files share
* Mon Feb 23 2004 - <niall.power@sun.com>
- install gconf schemas at the end of the install stage
