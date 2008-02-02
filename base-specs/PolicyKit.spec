# $Revision: 1.35 $, $Date: 2008-01-15 18:19:00 $
# TODO: package bash-completion in proper way
# nothing owns %{_datadir}/dbus-1/interfaces dir
Summary:	A framework for defining policy for system-wide components
Name:		PolicyKit
Version:	0.7
Release:	2
License:	MIT
Group:		Libraries
Source0:	http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	99e0cc588310656fa25f8f66a411c71f
Patch0:		%{name}-%{version}.diff
URL:		http://people.freedesktop.org/~david/polkit-spec.html
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.7
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	expat-devel >= 1:1.95.8
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libselinux-devel >= 1.30
BuildRequires:	libtool
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
Requires:	/usr/sbin/groupdel
Requires:	/usr/sbin/userdel
Requires:	/bin/id
Requires:	/usr/bin/getgid
Requires:	/usr/lib/rpm/user_group.sh
Requires:	/usr/sbin/groupadd
Requires:	/usr/sbin/useradd
Requires:	/usr/sbin/usermod
Requires:	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ConsoleKit >= 0.2.1
Provides:	group(polkituser)
Provides:	user(polkituser)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

%description -l pl.UTF-8
PolicyKit to szkielet do definiowania polityki dla komponentów
systemowych oraz składników pulpitu do konfigurowania ich. Jest
używany przez HAL-a.

%package apidocs
Summary:	PolicyKit API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
PolicyKit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API PolicyKit.

%package libs
Summary:	PolicyKit libraries
Group:		Libraries
Requires:	dbus-libs >= 1.0
Requires:	glib2 >= 1:2.6.0
Conflicts:	PolicyKit < 0.1-0.20061203.6

%description libs
PolicyKit libraries.

%description libs -l pl.UTF-8
Biblioteki PolicyKit.

%package devel
Summary:	Header files for PolicyKit
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	expat-devel >= 1:1.95.8
# polkit-grant
#Requires:	glib2-devel >= 1:2.6.0
# polkit-dbus and polkit-grant
#Requires:	dbus-devel >= 1.0
# polkit-dbus
#Requires:	libselinux-devel >= 1.30

%description devel
Header files for PolicyKit.

%description devel -l pl.UTF-8
Pliki nagłówkowe PolicyKit.

%package static
Summary:	Static PolicyKit libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PolicyKit libraries.

%description static -l pl.UTF-8
Statyczne biblioteki PolicyKit.

%prep
%setup -q
%patch0 -p1

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

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
autoconf
automake
./configure \
	--enable-maintainer-mode \
	--enable-gtk-doc \
	--prefix=/usr \
	--sysconfdir=/etc \
	--disable-tests \
	--with-polkit-user=polkitu \
	--with-polkit-group=polkitg \
	--with-os-type=solaris
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

make -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/PolicyKit/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerun -- PolicyKit < 0.3
%service -q PolicyKit stop
/sbin/chkconfig --del PolicyKit

%pre
%groupadd -g 220 polkituser
# %useradd -u 220 -d %{_datadir}/empty -c "PolicyKit User" -g polkituser polkituser

%post
umask 022
touch /var/lib/misc/PolicyKit.reload
chown root:polkituser /var/lib/misc/PolicyKit.reload
chmod 664 /var/lib/misc/PolicyKit.reload

%postun
if [ "$1" = "0" ]; then
	%userremove polkituser
	%groupremove polkituser
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc AUTHORS README doc/TODO
%attr(755,root,root) %{_bindir}/polkit-action
%attr(755,root,root) %{_bindir}/polkit-auth
%attr(755,root,root) %{_bindir}/polkit-config-file-validate
%attr(755,root,root) %{_bindir}/polkit-policy-file-validate
%dir %{_libexecdir}
%attr(2755,root,polkituser) %{_libexecdir}/polkit-explicit-grant-helper
%attr(2755,root,polkituser) %{_libexecdir}/polkit-grant-helper
%attr(4754,root,polkituser) %{_libexecdir}/polkit-grant-helper-pam
%attr(2755,root,polkituser) %{_libexecdir}/polkit-read-auth-helper
%attr(2755,root,polkituser) %{_libexecdir}/polkit-revoke-helper
%attr(2755,root,polkituser) %{_libexecdir}/polkit-set-default-helper
%attr(755,root,root) %{_libexecdir}/polkitd
%dir %{_sysconfdir}/PolicyKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PolicyKit/PolicyKit.conf
/etc/dbus-1/system.d/org.freedesktop.PolicyKit.conf
/etc/pam.d/polkit
%{_datadir}/PolicyKit
%{_datadir}/dbus-1/interfaces/org.freedesktop.PolicyKit.AuthenticationAgent.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.PolicyKit.service
%attr(664,root,polkituser) %ghost /var/lib/misc/PolicyKit.reload
%attr(770,root,polkituser) /var/lib/PolicyKit
%attr(775,root,polkituser) /var/lib/PolicyKit-public
%attr(770,root,polkituser) /var/run/PolicyKit
%{_mandir}/man1/polkit-action.1*
%{_mandir}/man1/polkit-auth.1*
%{_mandir}/man1/polkit-config-file-validate.1*
%{_mandir}/man1/polkit-policy-file-validate.1*
%{_mandir}/man5/PolicyKit.conf.5*
%{_mandir}/man8/PolicyKit.8*

%files apidocs
%defattr(-,root,root)
# %{_gtkdocdir}/polkit*.*

%files libs
%defattr(-,root,root)
# notes which license applies to which package part, AFL text (and GPL text copy)
%doc COPYING
%attr(755,root,root) %{_libdir}/libpolkit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit.so.2
%attr(755,root,root) %{_libdir}/libpolkit-dbus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit-dbus.so.2
%attr(755,root,root) %{_libdir}/libpolkit-grant.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit-grant.so.2

%files devel
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libpolkit.so
%attr(755,root,root) %{_libdir}/libpolkit-dbus.so
%attr(755,root,root) %{_libdir}/libpolkit-grant.so
%{_libdir}/libpolkit.la
%{_libdir}/libpolkit-dbus.la
%{_libdir}/libpolkit-grant.la
%{_includedir}/PolicyKit
# %{_pkgconfigdir}/polkit.pc
# %{_pkgconfigdir}/polkit-dbus.pc
# %{_pkgconfigdir}/polkit-grant.pc

%files static
%defattr(-,root,root)
%{_libdir}/libpolkit.a
%{_libdir}/libpolkit-dbus.a
%{_libdir}/libpolkit-grant.a

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* %{date} PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

$Log: PolicyKit.spec,v $
Revision 1.35  2008-01-15 18:19:00  patrys
- make it work on xfs

Revision 1.34  2007-12-16 03:23:38  qboosh
- more

Revision 1.33  2007-12-16 03:23:14  qboosh
- whole package is on MIT X11 license now

Revision 1.32  2007-12-16 03:22:47  qboosh
- updated to 0.7

Revision 1.31  2007-11-09 12:23:53  arekm
- rel 3; keep libexecdir binaries one level deeper in own subdirectory

Revision 1.30  2007-11-09 09:26:49  arekm
- rel 2; safer polkit-grant-helper-pam perms

Revision 1.29  2007/10/30 21:53:02  qboosh
- ConsoleKit version

Revision 1.28  2007/10/13 20:37:33  megabajt
- updated to 0.6

Revision 1.27  2007/09/18 17:56:58  patrys
- R: ConsoleKit

Revision 1.26  2007/09/08 17:08:45  patrys
- remove TODO

Revision 1.25  2007/09/08 17:05:22  patrys
- create user and group

Revision 1.24  2007/09/08 16:29:00  patrys
- package datadir

Revision 1.23  2007/09/08 13:47:31  qboosh
- cleanup, updated comments
- BR: libselinux-devel (for polkit-dbus library)

Revision 1.22  2007/09/08 09:26:29  tommat
- ver 0.5

Revision 1.21  2007/07/10 16:59:05  wolvverine
- rel. 2

Revision 1.20  2007/06/24 22:12:57  qboosh
- devel deps
- removed obsolete rc-scripts and chkconfig deps

Revision 1.19  2007/06/24 21:21:39  qboosh
- some cleanups and notes
- trigger to delete PolicyKit service on upgrade

Revision 1.18  2007/06/24 11:58:40  arekm
- parallel build broken

Revision 1.17  2007/06/21 12:52:46  patrys
- drop initscript (DBUS activation)
- FIXME: someone please write a trigger to remove the service on upgrade

Revision 1.16  2007/06/21 12:46:22  patrys
- 0.3

Revision 1.15  2007/03/14 16:52:51  czarny
- up to 20070314

Revision 1.14  2007/03/05 07:54:44  arekm
- rel .2

Revision 1.13  2007/02/13 06:46:49  glen
- tabs in preamble

Revision 1.12  2007/02/12 01:06:44  baggins
- converted to UTF-8

Revision 1.11  2006/12/09 13:27:17  qboosh
- actually it's 0.2 snapshot - updated Version, release .1
- polkit user/group not needed yet (not used for anything)

Revision 1.10  2006/12/09 13:10:04  qboosh
- libpolkit License is GPL v2 or AFL v2.1

Revision 1.9  2006/12/09 13:07:03  qboosh
- separated -libs, release .6

Revision 1.8  2006/12/06 22:37:55  arekm
- rel .5

Revision 1.7  2006/12/06 07:11:16  qboosh
- package gtkdoc
- more BRs/Rs

Revision 1.6  2006/12/05 22:03:41  arekm
- rel .4

Revision 1.5  2006/12/05 21:53:42  arekm
- rel .3

Revision 1.4  2006/12/05 21:29:16  patrys
- typo

Revision 1.3  2006/12/05 21:25:33  patrys
- added init

Revision 1.2  2006/12/05 20:02:43  qboosh
- pl, unified

Revision 1.1  2006/12/03 22:21:11  arekm
- new
