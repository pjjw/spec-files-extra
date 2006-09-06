#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEsnort
Summary:             Network intrusion prevention and detection system
Version:             2.6.0.1
Source:              http://www.snort.org/dl/current/snort-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SFEpcre
Requires: SFElibpcap

%prep
%setup -q -n snort-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/snort_dynamicengine/*.la

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

# Note: datadir is */share

%changelog
* 
* Fri Sep 01 2006 - Eric Boutilier
- Initial spec

