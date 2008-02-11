#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEntop
Summary:             A network traffic usage monitor
Version:             3.2
Source:              %{sf_download}/ntop/ntop-%{version}.tgz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibpcap-devel
BuildRequires: SFEgdbm-devel
BuildRequires: SFEgd-devel
Requires: SFElibpcap
Requires: SFEgdbm
Requires: SFEgd

Requires: %name-root

BuildRequires: SFEgawk

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n ntop-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%{_ldflags} -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --localstatedir=%{_localstatedir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*

%changelog
* Sat Mar 31 2007 - Thomas Wagner
- change Build-Requires to be SFEgd-devel
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Force gcc; adjust dependencies 
* Fri Sep 29 2006 - Eric Boutilier
- Initial spec
