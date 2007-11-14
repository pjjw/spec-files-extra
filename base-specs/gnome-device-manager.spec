#
# spec file for package gnome-device-manager
#
#
Name:         gnome-device-manager
License:      GPL
Group:        System/GUI
Version:      0.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Device-manager is a GNOME program to manage devices and device drivers.
Source0:      http://people.freedesktop.org/~david/dist/gnome-device-manager-%{version}.tar.bz2
Patch1:	      gnome-device-manager-01-build.diff
URL:          http://www.freedesktop.org/wiki/Software_2fhal
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: gnome-base-libs-devel
BuildRequires: gnome-python-libs-devel
BuildRequires: hal
Requires: gnome-base-libs
Requires: gnome-python-libs
Requires: hal
Requires: expat

%description
This is a GNOME program to manage devices and device drivers. It's
inspired by hal-device-manager, from the HAL project, but rewritten in
C for efficiency and an outlook to actually make it manage devices
rather than just show information.

%prep
%setup -q -n gnome-device-manager-%version
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

libtoolize --copy --force
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
			--datadir=%{_datadir} \
			--disable-scrollkeeper
make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
	
%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%clean 
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Remove %files sections.
* Mon Sep 17 2007 - trisk@acm.jhu.edu
- Add intltoolize to fix build
* Fri Aug 31 2007 - simon.zheng@sun.com
- Initialized.
