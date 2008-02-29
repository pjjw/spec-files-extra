#
# spec file for package SUNWgnome-display-mgr
#
# includes module(s): gdm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

Summary:                 GNOME display manager
Name:                    SUNWgnome-display-mgr
Version:                 2.21.8
Release:                 1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gdm/2.21/gdm-%{version}.tar.bz2
# Patch1 is a hack to work around the fact that the gio function
# g_file_info_get_attribute_string is returning a NULL on Solaris, causing
# the GDM GUI to crash.  This patch should be removed when gio is fixed to
# work properly on Solaris.
Patch1:                  gdm-01-fixgio.diff
# Patch2 adds SDTLOGIN interface, which drops the Xserver to user
# perms rather than running as root, for added security on Solaris.
Patch2:                  gdm-02-sdtlogin-devperm.diff
# Patch3 is probably not the right fix, but it seems that trying to set the
# default language to "C" is causing the GDM greeter to crash.
Patch3:                  gdm-03-fixcrash.diff
Patch4:                  gdm-04-logo-name.diff
Source1:                 gdm.xml
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWlibrsvg-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWlxml
BuildRequires: SUNWlibcroco
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWlibrsvg-devel
%if %option_without_fox
#
# GDM's configure depends on Xephyr to be installed so it properly
# sets Xnest configure option.
BuildRequires: SUNWxorg-server
Requires: SUNWxorg-server
Requires: SUNWxwplt
%else
# if SUNWxwplt is installed, then configure finds /usr/X11/bin/Xserver
# instead of /usr/X11/bin/Xorg
BuildConflicts: SUNWxwplt
%endif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-display-mgr-root
Requires: SUNWgnome-dialog
Requires: SUNWlibrsvg
Requires: SUNWlxml
Requires: SUNWlibcroco
Requires: SUNWpostrun
%if %option_with_dt
Requires: SUNWgnome-dtlogin-integration
%else
Requires: SUNWgnome-dtstart
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gdm-%version
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p1

%build
export LDFLAGS="%_ldflags -L/usr/openwin/lib -lXau -R/usr/openwin/lib -R/usr/sfw/lib"
export PKG_CONFIG_PATH=%{_pkg_config_path}
X11_CFLAGS=
pkg-config --exists x11 && X11_CFLAGS=`pkg-config --cflags x11`
export CFLAGS="%optflags $X11_CFLAGS"
export RPM_OPT_FLAGS="$CFLAGS"
%if %option_without_dt
export GDMGNOMESESSIONCMD="/usr/bin/dtstart jds"
%endif

%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="$RPM_OPT_FLAGS"
autoheader
autoconf

ENABLE_CONSOLE_HELPER=
%ifos linux
ENABLE_CONSOLE_HELPER="--enable-console-helper"
%endif

BINDIR_CONFIG=""
CTRUN_CONFIG=""
%ifos solaris
BINDIR_CONFIG="--with-post-path=/usr/openwin/bin"
RBAC_CONFIG="--enable-rbac-shutdown=solaris.system.shutdown"
%endif

libtoolize --force
glib-gettextize -c -f
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -a -c -f
./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --with-pam-prefix=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
        --disable-scrollkeeper \
        $ENABLE_CONSOLE_HELPER $BINDIR_CONFIG $RBAC_CONFIG
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int

make install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files
#
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/lib/scrollkeeper

install -d $RPM_BUILD_ROOT/var/svc/manifest/application/graphical-login
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/application/graphical-login

rmdir $RPM_BUILD_ROOT/etc/pam.d

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/*help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%post root
cat >> $BASEDIR/var/svc/profile/upgrade <<\EOF

# We changed gdm's FMRI.  If the old service exists and is enabled,
# disable it and enable the new one.
gdm=svc:/application/gdm2-login:default
if svcprop -q $gdm; then
	set -- `svcprop -C -t -p general/enabled $gdm`
	if [ $? -ne 0 ]; then
		echo "Could not read whether $gdm was enabled."
	elif [ $2 != boolean ]; then
		echo "general/enabled property of $gdm has bad type."
	elif [ $# -ne 3 ]; then
		echo "general/enabled property of $gdm has the wrong number\c"
		echo " of values."
	elif [ $3 = true ]; then
		svcadm disable $gdm
		svcadm enable svc:/application/graphical-login/gdm:default
	fi
fi

EOF

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%{_sbindir}/gdm-restart
%{_sbindir}/gdm-safe-restart
%{_sbindir}/gdm-stop
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo
%{_libexecdir}/gdm*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gdm
#%{_datadir}/gnome/help/gdm/C
%attr (-, root, other) %{_datadir}/icons
#%{_datadir}/omf/gdm/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/gnome-2.0/*
%{_datadir}/pixmaps/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*
%{_sysconfdir}/gconf
%dir %{_sysconfdir}/gdm
%{_sysconfdir}/gdm/*
# don't use %_localstatedir here, because this is an absolute path
# defined by another package, so it has to be /var/svc even if this
# package's %_localstatedir is redefined
%dir %attr (0755, root, sys) /var
/var/svc/*
%{_localstatedir}/gdm
%dir %attr (0755, root, sys) /var/log
%dir %attr (1770, root, gdm) /var/log/gdm
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (1770, root, gdm) %{_localstatedir}/lib/gdm
%{_localstatedir}/lib/gdm/.gconf.path
%{_localstatedir}/lib/gdm/.gconf.mandatory

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/*help/*/[a-z]*
%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%changelog
* Fri Feb 29 2008 - simon.zheng@sun.com
- Add patch 04-logo-icon.diff to fix greeter crach.
* Mon Feb 25 2008 - brian.cameron@sun.com
- Bump to 2.21.8.
* Wed Feb 20 2008 - brian.cameron@sun.com
- Add information about SDTLOGIN patch, which is currently
  not enabled.
* Sat Jan 26 2008 - brian.cameron@sun.com
- Created for 2.21 branch.
