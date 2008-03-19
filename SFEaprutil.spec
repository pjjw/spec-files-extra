#
# spec file for package SFElibapr
#
#
%include Solaris.inc
%include usr-gnu.inc

Name:			SFEaprutil
License:		Apache,LGPL,BSD
Version:		1.2.12
Summary:		Abstraction layer on top of Apache Portable Runtime
Source:			http://apache.mirrors.tds.net/apr/apr-util-%{version}.tar.gz
URL:			http://apr.apache.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWcsl
Requires: SUNWcsr
Requires: SFEgawk
Requires: SFElibapr
Requires: SUNWsqlite3
BuildRequires: SFElibapr-devel
BuildRequires: SUNWpostgr-devel
BuildRequires: SUNWsqlite3
BuildRequires: SUNWsfwhea

%description
Apache Portable Runtime (APR) provides software libraries
that provide a predictable and consistent interface to
underlying platform-specific implementations.

APR-util provides a number of helpful abstractions on top of APR.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWhea
Requires:                SFElibapr-devel
Requires:                SUNWpostgr-devel
Requires:                SUNWsqlite3
Requires:                SUNWsfwhea

%prep
%setup -q -n apr-util-%{version}

%build
export PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export CPPFLAGS="-I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L$RPM_BUILD_ROOT%{_libdir} -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --disable-static \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-threads \
    --with-apr=%{_prefix}/bin/apr-1-config \
    --with-dbm=gdbm \
    --with-gdbm=/usr \
    --with-pgsql=/usr \
    --with-sqlite3

# Unfortunate steps to work around a broken configure script
# that does not honour CFLAGS/CPPFLAGS/LDFLAGS when generating
# the Makefile
# configure is broken in other wasy as well. We need to specify
# *both* --with-dbm=gdbm and --with-gdbm... otherwise gdbm support
# is compiled with missing symbols due to config flags not being
# set properly!
#
[ ! -f Makefile.orig ] && cp Makefile Makefile.orig
cat Makefile | sed 's|INCLUDES =|INCLUDES = -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server|' > Makefile.new
cp Makefile.new Makefile
rm -f Makefile.new
cat Makefile | sed 's|APRUTIL_LIBS =|APRUTIL_LIBS = -L/usr/gnu/lib -R/usr/gnu/lib -liconv -lintl -L/usr/sfw/lib -R/usr/sfw/lib|' > Makefile.new
cp Makefile.new Makefile
rm -f Makefile.new

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
