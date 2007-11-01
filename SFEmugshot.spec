#
# spec file for package SFEmugshot
#
# includes module(s): mugshot
#
%include Solaris.inc

Name:                    SFEmugshot
Summary:                 Mugshot client
Version:                 1.1.56
Source:                  http://download.mugshot.org/client/sources/linux/mugshot-%{version}.tar.gz
Patch1:                  mugshot-01-xscreensaver.diff
Patch2:                  mugshot-02-nspr4.diff
Patch3:                  mugshot-03-Ispace.diff
Patch4:                  mugshot-04-__FUNCTION__.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEloudmouth-devel
BuildRequires: SFEcurl-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnutls-devel
BuildRequires: SUNWpcre
Requires: SUNWPython
Requires: SUNWgnutls
Requires: SUNWgnome-libs
Requires: SFEloudmouth
Requires: SUNWdbus
Requires: SFEcurl
Requires: SUNWpcre

%description
Mugshot is an open project to create a live social experience around
entertainment.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n mugshot-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/include/mps"
export CXXFLAGS="%cxx_optflags -I/usr/include/mps"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export LDFLAGS="%{_ldflags}"

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-gecko-idl=/usr/share/idl/firefox  \
            --with-gecko-headers=/usr/include/firefox \
            --with-xpidl=/usr/lib/firefox/xpidl

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/firefox/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/firefox/*/*/*.la

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/mugshot
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/icons
%{_datadir}/mugshot
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/ddm-1

%files root
%defattr (-, root, sys)
%{_sysconfdir}/gconf/schemas/mugshot-uri-handler.schemas

%changelog
* Mon Oct 29 2007 - brian.cameron@sun.com
- Add SFEpcre dependency.
* Sun Oct 14 2007 - laca@sun.com
- bump to 1.1.56
- add patches for various build issues
- update %files, add -devel subpkg
* Wed Oct 11 2006 - laca@sun.com
- fix icondir attributes
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEmugshot
- bump to 1.1.6
- fix build, %files, etc.
- define root subpkg, add gconf %post script
- update dependencies, file attributes
* Thu Jun  1 2006 - glynn.foster@sun.com
- Initial version
