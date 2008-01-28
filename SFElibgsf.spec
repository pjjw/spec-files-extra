#
# spec file for package SFElibgsf
#
# includes module(s): libgsf
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc
%use libgsf = libgsf.spec
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:                    SFElibgsf
Summary:                 A library provide i/o abstraction for dealing with different structured file formats
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: %{name}-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-vfs
Requires: SUNWbzip
Requires: SUNWpostrun
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-vfs-devel 
%if %option_with_gnu_iconv
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
BuildRequires: SFElibiconv-devel
Requires: SFEgettext
BuildRequires: SFEgettext-devel
%endif
%else
Requires: SUNWuiu8
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun

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

%build
export CFLAGS="%optflags -I/usr/gnu/include"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

%libgsf.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libgsf.install -d %name-%version

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

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
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/gsf-office-thumbnailer.schemas || retval=1';
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
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/gsf-office-thumbnailer.schemas || retval=1';
  echo 'exit $retval'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%attr (-, root, bin) %{_libdir}/python*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libgsf-1
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gsf-office-thumbnailer.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon jan 28 2008 - moinak.ghosh@sun.com
- Added a couple of missing dependencies.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Add check for presence on SUNWgnu-iconv and SUNWgnu-gettext packages.
* Thu Jan 03 2008 - nonsea@users.sourceforge.net
- Add gtk-doc check.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems.
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to CFLAGS/LDFLAGS
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Created.
