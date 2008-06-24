#
# spec file for package SFEgnucash
#
# includes module(s): gnucash
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use gnucash = gnucash.spec

Name:               SFEgnucash
Summary:            gnucash - Financial-accounting software
Version:            %{gnucash.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SFEguile
Requires:           SFEslib
BuildRequires:      SFEswig
BuildRequires:      SFEguile-devel

%package devel
Summary:            %{summary} - development files
SUNW_BaseDir:       %{_basedir}
%include default-depend.inc
Requires: %name


%if %build_l10n
%package l10n
Summary:            %{summary} - l10n files
SUNW_BaseDir:       %{_basedir}
%include default-depend.inc
Requires:           %{name}
%endif

%package root
Summary:            %{summary} - / filesystem
SUNW_BaseDir:       /
%include default-depend.inc
Requires:           SUNWpostrun-root
Requires:           SUNWgnome-config

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gnucash.prep -d %name-%version


%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export LDFLAGS="-lX11"
export RPM_OPT_FLAGS="$CFLAGS"
%gnucash.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnucash.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
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
  echo 'schemas="$SDIR/apps_gnucash*.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a


%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gmpc
%{_datadir}/gmpc/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*


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

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/apps_gnucash*.schemas


%changelog
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add BuildRequires SFEswig 
* Fri Jun 20 2008 - nonsea@users.sourceforge.net
- Move base part to gnucash.spec
- Add -root package
- Add %post and %postun for root
- Move .pc to -devel
- Add Requires/BuildRequires to SFEguile and SFEslib
* Mon Mar 10 2008 - nonsea@users.sourceforge.net
- Bump to 2.2.4
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
