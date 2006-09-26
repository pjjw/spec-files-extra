#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Note: This spec file will only work if CC is gcc. Do it at the command line
# before invoking this spec file (as opposed to putting it in %build below).
# That way the macros in Solaris.inc will know you've set it.

%include Solaris.inc

Name:                SFEganglia
Summary:             Ganglia cluster monitor, monitoring daemon
Version:             3.0.3
Source:              http://umn.dl.sourceforge.net/sourceforge/ganglia/ganglia-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgccruntime

# If gmetad support is desired, then see documentation about 
# needing rrdtool, etc. and uncomment the following line:
# BuildRequires: SFErrdtool
# Also see --with-gmetad below...

%prep
%setup -q -n ganglia-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

# If gmetad support is desired, enable:
#	    --with-gmetad
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
* 
* Sun Sep 24 2006 - Eric Boutilier
- Initial spec

