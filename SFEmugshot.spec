#
# spec file for package SFEmugshot
#
# includes module(s): mugshot
#
%include Solaris.inc

Name:                    SFEmugshot
Summary:                 Mugshot client
Version:                 1.1.6
Source:                  http://download.mugshot.org/client/sources/linux/mugshot-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEloudmouth-devel
BuildRequires: SFEcurl-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnutls-devel
Requires: SUNWPython
Requires: SUNWgnutls
Requires: SUNWgnome-libs
Requires: SFEloudmouth
Requires: SUNWdbus
Requires: SFEcurl

%description
Mugshot is an open project to create a live social experience around
entertainment.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun

%prep
%setup -q -n mugshot-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -lX11"
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

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

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
  echo 'schemas="$SDIR/mugshot-uri-handler.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/icons
%{_datadir}/mugshot
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}/gconf/schemas/mugshot-uri-handler.schemas

%changelog
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEmugshot
- bump to 1.1.6
- fix build, %files, etc.
- define root subpkg, add gconf %post script
- update dependencies, file attributes
* Thu Jun  1 2006 - glynn.foster@sun.com
- Initial version
