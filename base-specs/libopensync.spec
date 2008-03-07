#
# spec file for package libopensync
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
# bugdb: http://www.opensync.org/ticket/
#

Name:           libopensync
License:        GPL
Group:          System/Libraries
Version:        0.36
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.opensync.org/
Summary:        Data synchronization framework
Source:         http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc

%define         sqlite_version 3.0.0

Requires:       libxml2
Requires:       glib2
Requires:       sqlite         >= %{sqlite_version}

BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	swig-python
BuildRequires:	sqlite-devel    >= %{sqlite_version}

%description
OpenSync is a synchronization framework that is platform and
distribution independent.

It consists of several plugins that can be used to connect to devices,
a powerful sync-engine and the framework itself.

The synchronization framework is kept very flexible and is capable of
synchronizing any type of data, including contacts, calendar, tasks,
notes and files.

%package devel
Summary:		Header files, libraries and development documentation for %{name}
Group:			Development/Libraries
Requires:		%{name} = %{version}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q

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

%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr
%endif

make

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/osplugin
%dir %{_libdir}/opensync
%dir %{_libdir}/opensync/formats
%dir %{_libdir}/opensync/plugins
%dir %{_datadir}/opensync
%dir %{_datadir}/opensync/capabilities
%dir %{_datadir}/opensync/descriptions
%attr(755,root,root) %{_libdir}/opensync/formats/*.so
%{_libdir}/opensync/formats/*.la

%files devel
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/opensync*
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Jan 30 2008 - jijun.yu@sun.com
- Bump to 0.36
* Thu Dec 20 2007 - jijun.yu@sun.com
- Bump to 0.35
* Mon Nov 05 2007 - jijun.yu@sun.com
- Add the corret prefix option and remove Patch 1.
* Mon Nov 05 2007 - jijun.yu@sun.com
- Bump to 0.34
- Remove libopensync-01-add-glib.diff patch
- Add libopensync-01-prefix.diff patch 
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.33, change Source to full URL.
* Mon Aug 06 2007 - jijun.yu@sun.com
- Bump to 0.32
* Mon Jul 09 2007 - nonsea@users.sourceforge.net
- Bump to 0.31.
* Tue Jun 05 2007 - jijun.yu@sun.com
- Bump to 0.30
* Tue Apr  3 2007 - laca@sun.com
- bump to 0.22
- fix patch numbers
* Tue Nov 28 2006 - harry.lu@sun.com
- Add patch libopensync-05-null-crash.diff
* Tue Nov 14 2006 - halton.huo@sun.com
- Initial version
