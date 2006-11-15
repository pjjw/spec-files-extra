# The current version, 4.15, doesn't build... 
# with either gcc or Sun cc...
# TODO: Report the problem upstream
#
# This is version 3.02
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Relegating to /usr/gnu to avoid name collisions...
%define _prefix %{_basedir}/gnu

Name:                SFEsed
Summary:             GNU Stream Editor
Version:             3.02
Source:              ftp://ftp.gnu.org/gnu/sed/sed-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n sed-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#PATH=/opt/jdsbld/bin:/usr/ccs/bin:/usr/gnu/bin:/tmp/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --infodir=%{_datadir}/info

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%changelog
* 
* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
