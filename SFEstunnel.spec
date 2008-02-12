#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEstunnel
Summary:             An SSL client/server encryption wrapper
Version:             4.21
Source:              ftp://stunnel.mirt.net/stunnel/stunnel-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SUNWopenssl-libraries
Requires: SUNWopenssl-libraries
Requires: SUNWgccruntime

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n stunnel-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-ssl=/usr/sfw

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

install -D src/stunnel $RPM_BUILD_ROOT%{_sbindir}/stunnel
install -D src/.libs/libstunnel.so $RPM_BUILD_ROOT%{_libdir}/libstunnel.so
install -D doc/stunnel.8 $RPM_BUILD_ROOT%{_mandir}/man8/stunnel.8
install -D tools/stunnel.conf-sample $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.conf-sample

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man*/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/stunnel
%{_sysconfdir}/stunnel/stunnel.conf-sample

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 4.21
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Jan  7 2007 - laca@sun.com
- bump to 4.20
* Mon Dec 18 2006 - Eric Boutilier
- Initial spec
