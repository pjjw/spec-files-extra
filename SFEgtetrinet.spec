#
# spec file for package SFEtetrinet
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#

%include Solaris.inc

Name:                   SFEgtetrinet
Summary:                Client program for the popular Tetrinet game
Version:                0.7.11
Source:                 http://ftp.gnome.org/pub/GNOME/sources/gtetrinet/0.7/gtetrinet-%{version}.tar.gz

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-audio
Requires: SUNWlxml
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-audio-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:            %{summary} - / filesystem
SUNW_BaseDir:       /
%include default-depend.inc
Requires:           SUNWpostrun-root
Requires:           SUNWgnome-config

%prep
%setup -q -n gtetrinet-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export LDFLAGS="%_ldflags -lsocket -lnsl"
autoreconf
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir}	\
	    --disable-schemas-install	\
	    --enable-detach		\
	    --enable-ipv6


make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_prefix}/games/* $RPM_BUILD_ROOT%{_bindir}
rmdir $RPM_BUILD_ROOT%{_prefix}/games

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%include desktop-database-install.script
%include scrollkeeper-update.script
%include icon-cache.script

%postun
test -x $BASEDIR/lib/postrun || exit 0
%include desktop-database-uninstall.script
%include scrollkeeper-update.script
%include icon-cache.script

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
  echo 'schemas="$SDIR/gtetrinet.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gtetrinet
%{_datadir}/gtetrinet/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/gtetrinet.png
%dir %attr (0755, root, other) %{_datadir}/pixmaps/gtetrinet
%{_datadir}/pixmaps/gtetrinet/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_localedir}
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gtetrinet.schemas

%changelog
* Mon Jun 30 2008 - trisk@acm.jhu.edu
- Initial spec.
