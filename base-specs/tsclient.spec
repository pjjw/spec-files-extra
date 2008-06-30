#
# spec file for package tsclient
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=192483&atid=941574&aid=
#


Name:           tsclient
Summary:        a frontend for rdesktop and other remote desktop tools for the GNOME2 platform.
License:        GPL
Group:          User Interface/Desktops
Version:        0.150
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://sourceforge.net/projects/tsclient
Source:         http://%{sf_mirror}/%{name}/%{name}-%{version}.tar.gz
# date:2008-06-19 owner:halton type:bug bugid:1997801
Patch1:         %{name}-01-libsocket.diff
BuildRoot:      %{tmpdir}/%{name}-%{version}-root

Requires:	glib2 >= 2.0.0, gtk2 >= 2.0.0, rdesktop >= 1.3.0, vnc >= 4.0
BuildRequires:	glib2-devel >= 2.0.0, gtk2-devel >= 2.0.0


%description
Terminal Server Client is a frontend for rdesktop, vnc and other remote desktop tools.


%prep
%setup -q
%patch1 -p1


%build
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

aclocal $ACLOCAL_FLAGS
libtoolize --force
intltoolize --force --automake
autoheader
automake -a -f -c --gnu
autoconf

CFLAGS="$RPM_OPT_FLAGS"
./configure  --prefix=%{_prefix}         \
             --libdir=%{_libdir}         \
             --libexecdir=%{_libexecdir} \
             --datadir=%{_datadir}       \
             --mandir=%{_mandir}         \
             --sysconfdir=%{_sysconfdir} \
%if %debug_build
             --enable-debug=yes
%endif

make -j $CPUS


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog AUTHORS NEWS
%{_prefix}/bin/tsclient
%{_prefix}/libexec/tsclient-applet
%{_libdir}/bonobo/servers/GNOME_TSClientApplet.server
%{_datadir}/applications/tsclient.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/tsclient
%{_datadir}/locale/*/LC_MESSAGES/tsclient.mo
%{_datadir}/application-registry/tsclient.*
%{_datadir}/mime-info/tsclient.*
%{_datadir}/man/man1/tsclient.1*


%changelog
* Fri Jun 27 2008 - nonsea@users.sourceforge.net
- Add debug option 
* Thu Jun 19 2008 - nonsea@users.sourceforge.net
- Initial version
