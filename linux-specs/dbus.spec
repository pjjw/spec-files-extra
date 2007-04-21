#
# spec file for package dbus
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         dbus
License:      Other
Group:        System/Libraries
Version:      0.62
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Simple IPC library based on messages
Source:       http://dbus.freedesktop.org/releases/%{name}-%{version}.tar.gz
URL:          http://www.freedesktop.org/wiki/Software_2fdbus
Patch1:       dbus-01-glib_cflags.diff
Patch2:       dbus-02-python.diff
Patch3:       dbus-03-dbus-launch.diff
Patch4:       dbus-04-libexec.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define glib2_version 2.6.4
%define libxml2_version 2.6.19
%define python_version 2.4
BuildRequires: glib2-devel >= %glib2_version
BuildRequires: libxml2-devel >= %libxml2_version
# FIXME: get python rpm: BuildRequires: python >= %python_version
Requires: glib2 >= %glib2_version
Requires: libxml2 >= %libxml2_version

%description
D-BUS is a message bus system, a simple way for applications to talk to one
another.
D-BUS supplies both a system daemon (for events such as "new hardware device 
added" or "printer queue changed") and a per-user-login-session daemon (for 
general IPC needs among user applications). Also, the message bus is built on
top of a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message bus
daemon). 

%package devel
Summary:      Simple IPC library based on messages
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description devel
D-BUS is a message bus system, a simple way for applications to talk to one 
another.

D-BUS supplies both a system daemon (for events such as "new hardware device
added" or "printer queue changed") and a per-user-login-session daemon (for
general IPC needs among user applications). Also, the message bus is built on
top of a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message bus
daemon). 

%prep
%setup -q
%ifos solaris
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%endif

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
autoconf
automake-1.9 -a -c -f
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
            --localstatedir=%{_localstatedir} \
            --with-dbus-user=root       \
	    --mandir=%{_mandir}         \
            --disable-python            \
            --enable-mono
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dbus-1/services
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%config %{_sysconfdir}/dbus-1/session.conf
%config %{_sysconfdir}/dbus-1/system.conf
%{_bindir}/*
%{_libdir}/libdbus*.so*
%{_datadir}/man/*
%{_datadir}/dbus-1/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/dbus-1.0/*
%{_libdir}/dbus-1.0/*
%{_libdir}/pkgconfig/*
%{_libdir}/python?.?/vendor-packages/*

%changelog
* Sat Apr 21 2007 - dougs@truemail.co.th
- Forced automake-1.9

* Fri Jul 21 2006 - brian.cameron@sun.com
- Add patch to move dbus-daemon to /usr/lib, required by ARC.

* Tue May 02 2006 - laca@sun.com
- add patch console.diff that allows D-BUS to authenticate console user

* Sun Feb 26 2006 - laca@sun.com
- Bump to 0.61.
- move python stuff to vendor-packages, remove .pyo and *.la

* Thu Jan 19 2006 - damien.carbery@sun.com
- Remove upstream patch, 01-auth-external. Renumber remaining.

* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.60.

* Tue Oct 25 2005 - damien.carbery@sun.com
- Remove patch3 as an include dir under _libdir is okay. Bump to 0.50. Disable
  python bindings as they fail. Bug 4878 files at freedesktop.org.

* Fri Oct 21 2005 - damien.carbery@sun.com
- Add patches to build on Solaris.

* Tue Aug 30 2005 - glynn.foster@sun.com
- Create the dbus-1 services directory

* Tue Aug 16 2005 - damien.carbery@sun.com
- Add python >= 2.4 dependency. Reformat description text.

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.35.2.

* Mon Jun 20 2005 - matt.keenan@sun.com
- dbus 0.23 is actually shipped with gnome 2.10 so bumping down tarball

* Thu Jun 09 2005 - laca@sun.com
- add buildrequires glib2, libxml2

* Thu May 12 2005 - glynn.foster@sun.com
- Initial spec file for dbus.
