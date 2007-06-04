
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Note: This spec file will only work if CC is gcc. Do it at the command line
# before invoking this spec file (as opposed to putting it in %build below).
# That way the macros in Solaris.inc will know you've set it.

%include Solaris.inc

Name:                SFElibdaemon
Summary:             libdaemon
Version:             0.10
Source:              http://0pointer.de/lennart/projects/libdaemon/libdaemon-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libdaemon-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-I/usr/sfw/include -L/usr/sfw/lib -I/opt/sfw/include -L/opt/sfw/lib"
export CFLAGS="$CFLAGS -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"

export LDFLAGS="%{_ldflags} -lsocket -lnsl -L/usr/sfw/lib"
#fuer SunCC
#export LDFLAGS="-lsocket -lnsl -L/usr/sfw/lib"
#export LDFLAGS="-lsocket -lnsl -L/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --localstatedir=%{_localstatedir} \
	    --sysconfdir=%{_sysconfdir} \
            --disable-lynx

            

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon May 28 Thomas Wagner
- split into runtime and -devel
* 20070130 Thomas Wagner
- Initial spec

