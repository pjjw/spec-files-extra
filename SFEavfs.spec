#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEavfs
Summary:             Library for accessing virtual files (compressed, archived, remote, etc)
Version:             0.9.7
Source:              http://superb-west.dl.sourceforge.net/sourceforge/avf/avfs-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n avfs-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure \
        --prefix=%{_prefix}  \
        --mandir=%{_mandir}  \
        --enable-library     \
        --disable-preload    \
        --enable-static=no   \
        --with-ssl=/usr/sfw

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/libavfs.la
rm ${RPM_BUILD_ROOT}%{_bindir}/{dav,ftp}pass
rmdir ${RPM_BUILD_ROOT}%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/avfs-config
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/avfs
%{_libdir}/libavfs.so*
%{_libdir}/avfs/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/avfs.h
%{_includedir}/virtual.h

%changelog
* Tue Mar 20 2007 - daymobrew@users.sourceforge.net
- Remove from %install the code that removes the non-existant /usr/etc dir.

* Mon Mar 12 2007 - Eric Boutilier
- Initial spec
