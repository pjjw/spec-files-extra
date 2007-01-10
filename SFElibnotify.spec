#
# spec file for package SFElibnotify
#
# includes module(s): libnotify
#

%include Solaris.inc

Name:         SFElibnotify
License:      Other
Group:        System/Libraries
Version:      0.4.3
Summary:      libnotify is a notification system for the GNOME desktop environment.
Source:       http://www.galago-project.org/files/releases/source/libnotify/libnotify-%{version}.tar.bz2
URL:          http://www.galago-project.org/news/index.php
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
Requires: SUNWgnome-base-libs
Requires: SUNWdbus

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n libnotify-%version

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
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
		--libdir=%{_libdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%dir %attr (0755, root, bin) %dir %{_includedir}/libnotify
%{_includedir}/libnotify/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %dir %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Jan  7 2007 - laca@sun.com
- fix gtk-doc dir attributes
* Thu Nov 23 2006 - jedy.wang@sun.com
- Initial spec
