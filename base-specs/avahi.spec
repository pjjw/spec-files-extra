
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# NOTE: adds user "avahi" and group "avahi" - create before install, if you want
#       specific numeric UID/GID.

%include Solaris.inc

Name:                SFEavahi
Summary:             Avahi
Version:             0.6.21
Source:	    	     http://avahi.org/download/avahi-%{version}.tar.gz
Patch1:              avahi-01-dbus.diff
URL:                 http://avahi.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


BuildRequires: SFElibdaemon-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-bindings-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWPython
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
Requires: SUNWpostrun
Requires: SFElibdaemon
Requires: SUNWdbus
Requires: SUNWlexpt


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%package sharp
Summary:                 %{summary} -  mono .NET bindings
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
BuildRequires: SFEmono-devel
BuildRequires: SFEmonodoc
Requires: SFEmono
Requires: SFEgtk-sharp


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
#test#Requires: SUNWpostrun


%prep
%setup -q -n avahi-%version
%patch1 -p1


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%{optflags} -I/usr/sfw/include -L/usr/sfw/lib"
export CFLAGS="$CFLAGS -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"

export LDFLAGS="%{_ldflags} -lsocket -lnsl -L/usr/sfw/lib -R/usr/sfw/lib"

autoheader
autoconf
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --localstatedir=%{_localstatedir} \
	    --sysconfdir=%{_sysconfdir} \
            --enable-dbus \
            --disable-qt3 \
            --disable-qt4 \
            --disable-gdbm \
            --enable-dbm \
            --disable-autoipd \
            --enable-mono \
            --with-distro=none \
            --disable-static

            

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/usr/lib/*.la

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libavahi*
%{_libdir}/python2.4/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/avahi-client.pc
%{_libdir}/pkgconfig/avahi-core.pc
%{_libdir}/pkgconfig/avahi-glib.pc
%{_libdir}/pkgconfig/avahi-ui.pc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/avahi/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/avahi/*
%{_sysconfdir}/dbus-1/*

%files sharp
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, bin) %{_libdir}/monodoc
%{_libdir}/monodoc/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/avahi-sharp.pc
%{_libdir}/pkgconfig/avahi-ui-sharp.pc


#TODO# better error handling for (user|group)(add|del)

%post root
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'retval=0';
  echo 'getent group avahi || groupadd avahi';
  echo 'getent passwd avahi || useradd -d /tmp -g avahi avahi';
  echo 'NOTE: restarting d-bus:';
  echo 'svcadm restart system/dbus';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun root
( echo 'PATH=/usr/bin:/usr/sbin; export PATH' ;
  echo 'getent passwd avahi && userdel avahi';
  echo 'getent group avahi && groupdel avahi';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE


%changelog
* Mon Oct 08 2007 - trisk@acm.jhu.edu
- Turn into base-spec
* Sat Sep 01 2007 - trisk@acm.jhu.edu
- Add SFEavahi-sharp (seperate later)
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 0.6.21
- Allow dbus backwards compatibility.
* Mon Jun  4 2007 - Thomas Wagner
- NOTE: this spec is provided, just to get an idea of what 
  project nwam would do officially:
  http://opensolaris.org/os/project/nwam/service-discovery
- new postinstall: useradd avahi, groupadd avahi (create yourself
  before install, if you need a specific number for UID/GID !)
  svcadm restart system/dbus is done by postinstall-script too
  new postremove: groupdel avahi, userdel avahi
- NOTE: start avahi-daemon -D  yourself (no SMF integration)
* Mon May 28 2007 - Thomas Wagner
- bump to 0.6.19
* 20070405 Thomas Wagner
- refine spec
* 20070130 Thomas Wagner
- Initial spec and lots of fun

