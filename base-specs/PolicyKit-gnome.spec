# $Revision: 1.9 $, $Date: 2008-01-06 00:13:41 $
Summary:	GNOME dialogs for PolicyKit
Name:		PolicyKit-gnome
Version:	0.7
Release:	1
License:	LGPL v2+ (polkit-gnome library), GPL v2+ (D-Bus service)
Group:		X11/Applications
Source0:	http://hal.freedesktop.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	978ccbe3c9426f4d59c7903f566f954b
# Patch0:		%{name}-link.patch
URL:		http://people.freedesktop.org/~david/polkit-spec.html
BuildRequires:	PolicyKit-devel >= 0.7
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	gnome-common >= 2.0
BuildRequires:	gnome-vfs2-devel >= 2.4
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgnomeui-devel >= 2.14.0
BuildRequires:	libsexy-devel >= 0.1.11
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PolicyKit-gnome provides a D-BUS session bus service that is used to
bring up authentication dialogs used for obtaining privileges.

%description -l pl.UTF-8
Pakiet PolicyKit-gnome udostępnia usługę magistrali sesji D-BUS
służącą do wyświetlania okien dialogowych uwierzytelniania w celu
uzyskania uprawnień.

%package libs
Summary:	PolicyKit add-on library for GNOME
Group:		X11/Libraries
Requires:	PolicyKit-libs >= 0.7
Requires:	gtk+2 >= 2:2.12.0

%description libs
PolicyKit add-on library for GNOME.

%description libs -l pl.UTF-8
Dodatkowa biblioteka PolicyKit dla GNOME.

%package devel
Summary:	Header files for polkit-gnome library
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	PolicyKit-devel >= 0.7
Requires:	dbus-devel >= 1.0
Requires:	gtk+2-devel >= 2:2.12.0
Requires:	libselinux-devel >= 1.30

%description devel
Header files for polkit-gnome library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki polkit-gnome.

%package static
Summary:	Static polkit-gnome library
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static polkit-gnome library.

%description static -l pl.UTF-8
Statyczna biblioteka polkit-gnome.

%package demo
Summary:	Demo application for PolicyKit-gnome
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description demo
PolicyKit-gnome-demo provides a sample application that demonstrates
the features of both PolicyKit and PolicyKit-gnome. You normally don't
want to have this package installed.

%description demo -l pl.UTF-8
Pakiet PolicyKit-gnome-demo zawiera przykładową aplikację
demonstrującą możliwości pakietów PolicyKit i PolicyKit-gnome. Zwykle
ten pakiet nie powinien być instalowany.

%prep
%setup -q
# %patch0 -p1

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
	--prefix=/usr
make

%install
# rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS TODO
%attr(755,root,root) %{_bindir}/polkit-gnome-authorization
%attr(755,root,root) %{_libdir}/polkit-gnome-manager
%{_datadir}/dbus-1/services/org.gnome.PolicyKit.service
%{_datadir}/dbus-1/services/org.gnome.PolicyKit.AuthorizationManager.service
%{_datadir}/dbus-1/services/gnome-org.freedesktop.PolicyKit.AuthenticationAgent.service
# %{_desktopdir}/polkit-gnome-authorization.desktop

%files libs
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libpolkit-gnome.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit-gnome.so.0

%files devel
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libpolkit-gnome.so
%{_libdir}/libpolkit-gnome.la
%{_includedir}/PolicyKit/polkit-gnome
# %{_pkgconfigdir}/polkit-gnome.pc
# %{_gtkdocdir}/polkit-gnome

%files static
%defattr(-,root,root)
%{_libdir}/libpolkit-gnome.a

%files demo
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/polkit-gnome-example
%{_datadir}/PolicyKit/policy/polkit-gnome-example.policy

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* %{date} PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

$Log: PolicyKit-gnome.spec,v $
Revision 1.9  2008-01-06 00:13:41  megabajt
- run ldconfig in %post / %postun

Revision 1.8  2008-01-04 01:52:56  qboosh
- added link patch, fixed files
- release 1

Revision 1.7  2007-12-16 03:44:14  qboosh
- up to 0.7 (not tested)

Revision 1.6  2007-10-30 21:48:02  qboosh
- updated pl (lazy developers :/)

Revision 1.5  2007/10/17 13:37:13  megabajt
- added demo subpackage and TODO
- release 1

Revision 1.4  2007/10/13 20:48:07  megabajt
- updated to 0.6
- release 0.1 NFY

Revision 1.3  2007/09/08 16:07:56  patrys
- 0.5

Revision 1.2  2007/09/08 13:48:37  qboosh
- updated Source URL

Revision 1.1  2007/07/07 23:24:13  qboosh
- new
