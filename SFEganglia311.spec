#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEganglia
Summary:             Ganglia cluster monitor, monitoring daemon
Version:             3.1.1
Source:              %{sf_download}/ganglia/ganglia-%{version}.tar.gz
#Patch1:              ganglia-01-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgccruntime
Requires: SFEcheck
BuildRequires: SFEcheck

# If gmetad support is desired, then see documentation about
# needing rrdtool, etc. and uncomment the following line:
# BuildRequires: SFErrdtool
# Also see --with-gmetad below...

%prep
%setup -q -n ganglia-%version
#%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=cc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -R/usr/apr/1.3/lib -L/usr/apr/1.3/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
         --with-gmetad

# If gmetad support is desired, enable:
#         --with-gmetad
# and see doc about needing rrdtool...

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libganglia.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libganglia.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Force gcc
* Sun Sep 24 2006 - Eric Boutilier
- Initial spec
