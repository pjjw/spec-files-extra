#
# spec file for package SUNWsqlite
#
# includes module(s): sqlite
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc

%use sqlite = sqlite.spec

Name:           SUNWsqlite
Summary:        SQLite - a C library that implements an embeddable SQL database engine
Version:        %{default_pkg_version}
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%sqlite.prep -d %name-%version

%build

if [ "x`basename $CC`" != xgcc ]
then
	MTFLAG="-mt"
else
	MTFLAG=
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags $MTFLAG -DSOLARIS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_REENTRANT -D_POSIX_PTHREAD_SEMANTICS -D_FILE_OFFSET_BITS=64 -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ -DSQLITE_ENABLE_REDEF_IO"
export LDFLAGS="%{_ldflags}"
export RPM_OPT_FLAGS="$CFLAGS"
%sqlite.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%sqlite.install -d %name-%version
cd %{_builddir}/%name-%version

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
* Sat Jan 12 2008 - moinak.ghosh@sun.com
- Fix build with gcc
* Wed Jan 02 2008 - nonsea@users.sourceforge.net
- Rename from SFEsqlite to SUNWsqlite.
* Mon Nov 12 2007 - nonsea@users.sourceforge.net
- Spilit into sqlite.spec
- Tue Oct 09 2007 - brian.cameron@sun.com
- Revert back to 3.4.2.  Found crashing problems running the examples
  in pysqlite with the 3.5.1 version.
* Fri Oct 05 2007 - brian.cameron@sun.com
- Bump to 3.5.1
* Mon Sep 17 2007 - nonsea@users.sourceforge.net
- Add -DSQLITE_ENABLE_REDEF_IO to CFLAGS for firefox3.
* Thu Sep 06 2007 - nonsea@users.sourceforge.net
- Bump to 3.4.2, 3.5.0 is still alpha.
- Uncomment patch1.
* Wed Sep 05 2007 - nonsea@users.sourceforge.net
- Bump to 3.5.0
- Comment patch1, seems no crash when run sqlite and opensync,
  will contact patch owner laca.
* Mon Jul 30 2007 - markwright@internode.on.net
- Bump to 3.4.1
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Add --enable-threads-override-locks and --disable-debug option for tracker.
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Bump to 3.3.17.
* Wed Feb 28 2007 - markgraf@med.ovgu.de
- bump to 3.3.13 as source for 3.3.8 is no longer available
* Tue Nov 11 2006 - halton.huo@sun.com
- Rename from SUNWsqlite3 to SUNWsqlite
- Bump to 3.3.8
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 3.3.7
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
