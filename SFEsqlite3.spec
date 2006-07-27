#
# spec file for package SFEsqlite3
#
# includes module(s): sqlite3
#
%include Solaris.inc
Name:                    SFEsqlite3
Summary:                 SQLite - a small C library implementation of a SQL database engine
Version:                 3.3.6
Source:                  http://www.sqlite.org/sqlite-%{version}.tar.gz
Patch1:                  sqlite3-01-thread-lock-test.diff
URL:                     http://www.sqlite.org/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n sqlite-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -mt -DSOLARIS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT -D_POSIX_PTHREAD_SEMANTICS -D_FILE_OFFSET_BITS=64 -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} --enable-static=no \
       --enable-releasemode --enable-threadsafe --disable-tcl \
       --disable-cross-thread-connections --enable-tempstore \
	--mandir=%{_mandir} --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --includedir=%{_includedir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make BASENAME=${RPM_BUILD_ROOT}%{_prefix}	\
     MANDIR=${RPM_BUILD_ROOT}%{_mandir} DESTDIR=$RPM_BUILD_ROOT install
strip ${RPM_BUILD_ROOT}%{_bindir}/*

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

cd ${RPM_BUILD_ROOT}%{_libdir}
ln -s libsqlite3.so libsqlite3.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*

%files devel 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Mon Jul 10 2006 - laca@sun.com
- rename to SFEsqlite3
- move to /usr
- update file attributes
- delete unnecessary env variables
- add patch thread-lock-test.diff: it disables a thread locking behaviour
  test on Solaris and hardcodes the result of the test, which I obtained
  by separating this code into a test program.  The thread operations
  in this test conflict with thread operations in the hans boehm garbage
  collector and crash mono apps that attempt to use sqlite3.
* Fri Mar 17 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
