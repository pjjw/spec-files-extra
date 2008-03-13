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
Patch1:		PolicyKit-01-solaris.diff
Patch2:		PolicyKit-02-dirfd.diff
Patch3:		PolicyKit-03-rbac.diff
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
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	--prefix=%{_prefix} \
	--libdir=%{_libdir}/polkit \
	--libexecdir=%{_libdir}/polkit \
	--sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
	--disable-tests \
	--with-polkit-user=polkitu \
	--with-polkit-group=polkitg \
	--with-os-type=solaris \
	--with-auth-source=rbac \
	--enable-rbac-root
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

%changelog
* Wed Feb 06 2008 - brian.cameron@sun.com
- Cleanup
* Sat Feb 02 2008 - jim.li@sun.com
- Created.
