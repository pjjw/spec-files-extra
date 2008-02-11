#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibrsync
Summary:             Library for generating network deltas
Version:             0.9.7
Source:              %{sf_download}/librsync/librsync-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n librsync-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# Use gcc...
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no \
            --enable-shared=yes

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/librsync.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h

%changelog
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Thu Dec 21 2006 - Eric Boutilier
- Initial spec
