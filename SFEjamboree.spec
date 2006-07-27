#
# spec file for package SFEjamboree
#
# includes module(s): jamboree
#

%include Solaris.inc

Name:         SFEjamboree
Summary:      Jamboree Audio Player
License:      GPL
Group:        System/GUI/GNOME
Version:      0.5.9
Release:      1
#FIXME: where is this tarball from?!?
Source:       http://ftp.gnome.org/pub/GNOME/sources/jamboree/0.5/jamboree-%{version}.tar.bz2
Patch1:       jamboree-01-sunaudiosink.diff
URL:          http://developer.imendio.com/wiki/Jamboree
SUNW_BaseDir: %{_prefix}
BuildRoot:    %{_tmppath}/jamboree-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SFElibid3tag-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SFEgdbm-devel
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-media
Requires: SFElibid3tag
Requires: SUNWdbus
Requires: SFEgdbm
Requires: %name-root

%description
Jamboree is an audio player for the GNOME desktop, allowing you to play CDs,
and a wide range of multimedia formats

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n jamboree-%version
## Patch is for version 0.6.
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export LDFLAGS="%_ldflags -lX11"
export CFLAGS="%optflags"

libtoolize --force
intltoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir}         \
        --localstatedir=/var/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
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
  echo 'schemas="$SDIR/jamboree.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -i -c JDS -a

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || exit 0';
  echo 'rm -f %{_datadir}/icons/*/icon-theme.cache' ;
  echo 'ls -d %{_datadir}/icons/* | xargs -l1 /usr/bin/gtk-update-icon-cache'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -t 5

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/jamboree
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/jamboree.service

%files root
%defattr(0755, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/jamboree.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jul  4 2006 - laca@sun.com
- rename to SFEjamboree
- add l10n pkg
- delete -share subpkg
- delete lots of unnecessary deps and env variables
- update file attributes
* Mon May 08 2006 - damien.carbery@sun.com
- Bump to 0.5.9, a tarball from cvs, while waiting for 0.6 release.
* Thu Apr 06 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Thu Mar 09 2006 - brian.cameron@sun.com
- Created
