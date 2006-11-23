#
# spec file for package SFEnotification-daemon
#
# includes module(s): notification-daemon
#

%include Solaris.inc

Name:         SFEnotification-daemon
License:      Other
Group:        System/Libraries
Version:      0.3.6
Summary:      A notification daemon for the GNOME desktop environment.
Source:       http://www.galago-project.org/files/releases/source/notification-daemon/notification-daemon-%{version}.tar.bz2
URL:          http://www.galago-project.org/news/index.php
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SFElibsexy-devel
Requires: SUNWgnome-base-libs
Requires: SUNWdbus
Requires: SUNWgnome-panel
Requires: SUNWlibpopt
Requires: SFElibsexy

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n notification-daemon-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
		--libexecdir=%{_libexecdir} \
		--sysconfdir=%{_sysconfdir} \
		--libdir=%{_libdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%dir %attr (0755, root, bin) %dir %{_libdir}/notification-daemon-1.0
%dir %attr (0755, root, bin) %dir %{_libdir}/notification-daemon-1.0/engines
%{_libdir}/notification-daemon-1.0/engines/*.so*
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/notification-daemon
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/org.freedesktop.Notifications.service
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/nl

%files root
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/notification-daemon.schemas

%changelog
* Thu Nov 23 2006 - jedy.wang@sun.com
- Initial spec
