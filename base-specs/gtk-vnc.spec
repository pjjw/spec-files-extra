#
# spec file for package gtk-vnc
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#


Name:           gtk-vnc
License:        LGPL
Group:          Development/Libraries
Version:        0.3.6
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://gtk-vnc.sf.net/
Summary:        A GTK widget for VNC clients
Source:         http://%{sf_mirror}/sourceforge/%{name}/%{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel pygtk2-devel python-devel

%description
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package devel
Summary: Libraries, includes, etc. to compile with the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: pkgconfig
Requires: pygtk2-devel gtk2-devel

%description devel
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%package python
Summary: Python bindings for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description python
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

A module allowing use of the GTK-VNC widget from python

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
			--bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--libdir=%{_libdir} \
			--datadir=%{_datadir} \
			--includedir=%{_includedir} \
			--sysconfdir=%{_sysconfdir} \
%if %debug_build
			--enable-debug=yes \
%endif
	

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
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%doc examples/gvncviewer.c
%{_libdir}/lib*.so
%dir %{_includedir}/%{name}-1.0/
%{_includedir}/%{name}-1.0/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc

%files python
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%doc examples/gvncviewer.py
%{_libdir}/python*/site-packages/gtkvnc.so

%changelog
* Tue May 06 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.6
- Remove upsteamed patch solaris-ld-ast.diff
* Tue Apr 22 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.5
* Fri Mar 07 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.4
* Wed Feb 20 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.3
- Remove upstreamed patch suncc-range-case.diff
* Thu Jan 10 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.2
- Add patch suncc-range-case.diff to fix build issue.
* Fri Dec 14 2007 - nonsea@users.sourceforge.net
- Bump to 0.3.1
* Thu Dec 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.3.0
- Remove upsreamed patches: makefile.diff, macro.diff,
  yield.diff and coroutine.diff
- Add new patch solaris-ld-ast.diff
* Tue Oct 30 2007 - nonsea@users.sourceforge.net
- Add debug option.
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Initial version
