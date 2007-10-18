#
# spec file for package SFExchat
#
# includes module(s): xchat
#
%include Solaris.inc

# build with dbus support unless --without-dbus is used
%define with_dbus %{?_without_dbus:0}%{?!_without_dbus:1}

Name:                    SFExchat
Summary:                 XChat IRC Client
Version:                 2.8.4
Source:                  http://www.xchat.org/files/source/2.8/xchat-%{version}.tar.bz2
Patch1:                  xchat-01-gettext.diff
Patch2:                  xchat-02-zero-index.diff
Patch3:                  xchat-03-dbus-LDADD.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: CBEbison
BuildRequires: SUNWPython
Requires: SUNWgnome-libs
%if %{with_dbus}
Requires: SUNWdbus
Requires: %name-root
BuildRequires: SUNWdbus-devel
%endif

%if %{with_dbus}
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xchat-%version
%patch1 -p1 -b .patch01
%patch2 -p1 -b .patch02
%patch3 -p1 -b .patch03
touch NEWS

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/gnu/include -DANSICPP"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib -L/usr/gnu/lib -R/usr/gnu/lib"

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

%if %with_dbus
%define dbus_opt --enable-dbus
%else
%define dbus_opt --disable-dbus
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            %dbus_opt                        \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/xchat/plugins/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with_dbus}
%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/apps_xchat_url_handler.schemas'
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
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/apps_xchat_url_handler.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun
%endif

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%if %{with_dbus}
%{_datadir}/dbus-1/services/org.xchat.*
%endif

%if %{with_dbus}
%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/apps_xchat_url_handler.schemas
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to CFLAGS/LDFLAGS
* Thu Aug 02 2007 - Brian Cameron <brian.cameron@sun.com>
- Bump to 2.8.4.
* Tue May 29 2007 - Thomas Wagner
- bump to 2.8.2
- /usr/bin/msgfmt errors, use /opt/sfw/bin/msgfmt
- reworked patch for 2.8.2
* Sun Jan  7 2007 - laca@sun.com
- bump to 2.8.0, merge patches, update %files
* Mon Jul 31 2006 - glynn.foster@sun.com
- bump to 2.6.6
* Mon Jun 12 2006 - laca@sun.com
- bump to 2.6.4
- rename to SFExchat
- add -l10n pkg
- change to root:bin to follow other JDS pkgs.
- add patch that fixes the proxy in 2.6.4
* Fri Jun  2 2006 - laca@sun.com
- use post/postun scripts to install schemas into the merged gconf files
- merge -share pkg into base
* Thu Apr 20 2006 - damien.carbery@sun.com
- Bump to 2.6.2.
* Mon Mar 20 2006 - brian.cameron@sun.com
- Remove unneeded intltoolize call.
* Thu Jan 26 2006 - brian.cameron@sun.com
- Update to 2.6.1
* Wed Dec 07 2005 - brian.cameron@sun.com
- Update to 2.6.0
* Wed Oct 12 2005 - laca@sun.com
- update to 2.4.5; fix
* Thu Jan 06 2004 - Brian.Cameron@sun.com
- created
