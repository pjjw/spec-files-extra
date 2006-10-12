#
# spec file for package SFEbaobab
#
# includes module(s): baobab
#

%include Solaris.inc

Name:                    SFEbaobab
Summary:                 Baobab - disk usage analyser for the GNOME desktop
Version:                 2.4.2
Source:                  http://www.marzocca.net/linux/downloads/baobab-%{version}.tar.gz
URL:                     http://www.marzocca.net/linux/baobab.html
Patch1:			 baobab-01-export-dynamic.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWlibgtop
Requires: SUNWpostrun
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWlibgtop-devel

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
%setup -q -n baobab-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS 

%install
make DESTDIR=$RPM_BUILD_ROOT install

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || exit 0';
  echo 'ls -d %{_datadir}/icons/hicolor/* | xargs -l1 /usr/bin/gtk-update-icon-cache'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -t 15

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:/etc/gconf/gconf.xml.defaults';
  echo 'export GCONF_CONFIG_SOURCE';
  echo '/usr/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -u -c JDS_wait

%preun root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$PKG_INSTALL_ROOT/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$PKG_INSTALL_ROOT%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/baobab.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -i -c SFE -a

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (-, root, bin) %{_bindir}/baobab
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/baobab.desktop
%dir %attr (0755, root, other) %{_datadir}/baobab
%dir %attr (0755, root, other) %{_datadir}/baobab/pixmaps
%{_datadir}/baobab/pixmaps/*
%attr (-, root, other) %{_datadir}/icons
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/baobab.1

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/baobab.schemas

%changelog
* Wed Oct 11 2006 - laca@sun.com
- fix icondir permissions
* Thu Jul 06 2006 - laca@sun.com
- rename to SFEbaobab
* Thu Jul 06 2006 - matt.keenan@sun.com
- Initial spec file
