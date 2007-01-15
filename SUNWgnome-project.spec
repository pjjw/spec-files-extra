#
# spec file for package SUNWgnome-project
#
# includes module(s): gnome-project
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%use libgsf = libgsf.spec
%use planner = planner.spec

Name:                    SUNWgnome-project
Summary:                 GNOME Project Planner
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-project-root
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWPython
Requires: SUNWgnome-python-libs
Requires: SUNWbzip
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-print
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWzlib
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWPython-devel
Requires: SUNWpostrun

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

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
%libgsf.prep -d %name-%version
%planner.prep -d %name-%version

%build
export PKG_CONFIG_PATH=../libgsf-%{libgsf.version}:%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%libgsf.build -d %name-%version
%planner.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libgsf.install -d %name-%version
%planner.install -d %name-%version

rmdir $RPM_BUILD_ROOT%{_datadir}/omf

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
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
  echo 'retval=0';
  echo 'for schemas in gsf-office-thumbnailer planner; do \';
  echo '  /usr/bin/gconftool-2 --makefile-install-rule $SDIR/$schemas.schemas || retval=1';
  echo 'done';
  echo 'exit $retval'
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
  echo 'retval=0';
  echo 'for schemas in gsf-office-thumbnailer planner; do \';
  echo '  /usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/$schemas.schemas || retval=1';
  echo 'done';
  echo 'exit $retval'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/planner/file-modules/lib*.so*
%{_libdir}/planner/plugins/lib*.so*
%{_libdir}/planner/storage-modules/lib*.so*
%attr (-, root, bin) %{_libdir}/python*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/planner/C
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*png
%{_datadir}/planner
%attr (-, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files devel
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libgsf-1
%{_includedir}/planner-1.0
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gsf-office-thumbnailer.schemas
%{_sysconfdir}/gconf/schemas/planner.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/[a-z]*
%endif

%changelog
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Correct rm line for non-l10n builds. It was deleting way too much.
* Sat Oct 14 2006 - laca@sun.com
- fix /usr/share/gnome attributes in l10n subpkg
* Wed Oct 11 2006 - laca@sun.com
- fix icondir permissions
* Sun Jul 23 2006 - laca@sun.com
- move to /usr
* Fri Jun  2 2006 - laca@sun.com
- use post/postun scripts to install schemas into the merged gconf files
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Wed Nov 30 2005 - damien.carbery@sun.com
- Add Build/Requires on SUNWPython/-devel and SUNWgnome-python-libs/-devel.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Sep 30 2005 - damien.carbery@sun.com
- Remove javahelp-convert references: no longer used. Fix %files perms for some
  dirs. Delete some %gconf.xml files.
* Tue Sep 20 2005 - laca@sun.com
- update python paths
* Fri Sep 17 2005 - laca@sun.com
- define root subpkg; install gconf files; remove unpackaged files
* Tue May 24 2005 - brian.cameron@sun.com
- Bump to 2.10, fix packaging.
* Fri Jan 28 2005 - matt.keenan@sun.com
- #6222336 - Don't ship planner omf files
* Mon Dec 13 2004 - damien.carbery@sun.com
- Move to /usr/sfw to implement ARC decision.
* Fri Nov 12 2004 - laca@sun.com
- move to /usr/demo/jds
* Wed Oct 06 2004 - matt.keenan@sun.com
- added l10n help files section
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Tue Aug 31 2004 - shirley.woo@sun.com
- Bug 5091588 :Added BuildRequires SUNWlibpopt-devel since SUNWlibpopt
  was split
* Wed Aug 25 2004 - brian.cameron@sun.com
- Corrected packaging after adding gtk-docs to planner.spec
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Mon Jul 26 2004 - damien.carbery@sun.com
- Add SUNWgnome-print as BuildRequires.
* Sat Jun 26 2004 - shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Mon Apr 12 2004 - brian.cameron@sun.com
- Created,
