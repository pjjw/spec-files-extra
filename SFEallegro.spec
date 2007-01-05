#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Relegating to /usr/gnu to avoid name collision with /usr/bin/pack:
%define _prefix %{_basedir}/gnu

Name:                SFEallegro
Summary:             Game programming library
Version:             4.2.1
Source:              http://umn.dl.sourceforge.net/sourceforge/alleg/allegro-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-audio
Requires: SUNWxwplt
Requires: SUNWgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n allegro-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointers"

export LDFLAGS="%{_ldflags} -R/usr/gnu/lib"

# The following on-the-fly patch is applied because this source's makefile
# uses syntax that works with bash(1) but not sh(1); yet makefile.in
# hardcodes SHELL = /bin/sh (and likely gets away with it because /bin/sh
# on some (all?) Linux systems is symlink'd to /bin/bash.)
# TODO: Report this upstream

perl -i.orig -lpe 's/^(SHELL = \/bin\/sh).*/#$1/ and print "SHELL = /bin/bash"' makefile.in

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install     DESTDIR=$RPM_BUILD_ROOT
make install-man DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, other) %{_includedir}/allegro
%{_includedir}/allegro/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Fri Jan 05 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Bump to 4.2.1.
* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
