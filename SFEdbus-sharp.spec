#
# spec file for package SFEdbus-sharp
#
# includes module(s): dbus (mono bindings only)
#

%include Solaris.inc

%use dbus = dbus.spec

Name:                    SFEdbus-sharp
Summary:                 Simple IPC library based on messages - mono .NET bindings
Version:                 %{dbus.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWdbus
BuildRequires:  SFEmono-devel
Requires:       SFEmono
Requires:       SFEgtk-sharp

%prep
rm -rf %name-%version
mkdir %name-%version
%dbus.prep -d %name-%version

%build
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/gnu/include"
export RPM_OPT_FLAGS=$CFLAGS
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lexpat -L/usr/gnu/lib -R/usr/gnu/lib"
# put /usr/ccs/lib first in the PATH so that cpp is picked up from there
# note: I didn't put /usr/lib in the PATH because there's too much other
# stuff in there
export PATH=/usr/ccs/lib:/usr/mono/bin:$PATH
%dbus.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
export PATH=/usr/mono/bin:$PATH
%dbus.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}
rm -rf $RPM_BUILD_ROOT%{_localstatedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*
rm -f $RPM_BUILD_ROOT%{_libdir}/dbus-daemon
rm -rf $RPM_BUILD_ROOT%{_libdir}/dbus-1.0
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_datadir}/dbus-1
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/dbus-1.pc
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/dbus-glib-1.pc
rmdir $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/mono
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to search paths
* Fri Jul 21 2006 - laca@sun.com
- created, based on SUNWdbus.spec but with mono enabled and python disabled

