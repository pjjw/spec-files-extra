#
# spec file for package SFEavahi-sharp
#
# includes module(s): avahi (mono bindings only)
#

%include Solaris.inc

%use avahi = avahi.spec

Name:                    SFEavahi-sharp
Summary:                 Avahi - mono .NET bindings
Version:                 %{avahi.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWavahi-bridge-dsd-devel
Requires:	SUNWavahi-bridge-dsd
BuildRequires:  SFEmono-devel
Requires:       SFEmono
Requires:       SFEgtk-sharp

%prep
rm -rf %name-%version
mkdir %name-%version
%avahi.prep -d %name-%version

%build
export CFLAGS="%{optflags} -I/usr/sfw/include -L/usr/sfw/lib"
export CFLAGS="$CFLAGS -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"
export LDFLAGS="%{_ldflags} -lsocket -lnsl -L/usr/sfw/lib -R/usr/sfw/lib"
# put /usr/ccs/lib first in the PATH so that cpp is picked up from there
# note: I didn't put /usr/lib in the PATH because there's too much other
# stuff in there
export PATH=/usr/ccs/lib:/usr/mono/bin:$PATH
%avahi.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
export PATH=/usr/mono/bin:$PATH
%avahi.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_sbindir}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*
rm -rf $RPM_BUILD_ROOT%{_libdir}/python2.4
rm -rf $RPM_BUILD_ROOT%{_libdir}/avahi
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/avahi-client.pc
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/avahi-core.pc
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/avahi-glib.pc
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/avahi-ui.pc
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_datadir}/avahi
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rmdir $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, bin) %{_libdir}/monodoc
%{_libdir}/monodoc/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Oct 08 2007 - trisk@acm.jhu.edu
- Created, based on SFEavahi.spec

