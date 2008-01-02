#
# spec file for package sqlite
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:           sqlite
License:        Public Domain
Group:          System/Libraries
Version:        3.5.4
Release:        4
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.sqlite.org
Summary:        SQLite - a C library that implements an embeddable SQL database engine
Source:         http://www.sqlite.org/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process. The distribution comes with a
standalone command-line access program (sqlite) that can be used to
administer an SQLite database and which serves as an example of how to
use the SQLite library.

%package devel
Summary: Header files and libraries for developing apps which will use %{name}
Group: Development/C
Requires: %{name} = %{version}-%{release}

%description devel
The sqlite-devel package contains the header files and libraries needed
to develop programs that use the sqlite database library.

%prep
%setup -q -n %{name}-%{version}

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

./configure --prefix=%{_prefix} \
			--bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--libdir=%{_libdir} \
			--datadir=%{_datadir} \
			--includedir=%{_includedir} \
			--sysconfdir=%{_sysconfdir} \
			--enable-static=no                  \
			--enable-releasemode                \
			--enable-threadsafe                 \
			--disable-tcl                       \
			--disable-cross-thread-connections  \
			--enable-tempstore                  \
			--enable-threads-override-locks     \
			--disable-debug                     \

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/sqlite3.pc
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*

%changelog
* Mon Nov 12 2007 - nonsea@users.sourceforge.net
- Bump to 3.5.2.
- Remove upstreamed patch thread-lock-test.diff.
- Initial version, spilit from SFEsqlite.spec
