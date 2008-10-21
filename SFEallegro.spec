#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

# Relegating to /usr/gnu to avoid name collision with /usr/bin/pack:
%include usr-gnu.inc

Name:                SFEallegro
Summary:             Game programming library
Version:             4.2.2
Source:              %{sf_download}/alleg/allegro-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
Group:               Games
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-audio
%if %(pkginfo -q FSWxwrtl && echo 1 || echo 0)
# using FOX
Requires: FSWxwrtl
%else
Requires: SUNWxwplt
%endif
Requires: SUNWgccruntime
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWbash

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
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
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer -I/usr/X11/include"

export LDFLAGS="%{_ldflags} -R/usr/gnu/lib"

# The following on-the-fly patch is applied because this source's makefile
# uses syntax that works with bash(1) but not sh(1); yet makefile.in
# hardcodes SHELL = /bin/sh (and likely gets away with it because /bin/sh
# on some (all?) Linux systems is symlink'd to /bin/bash.)
# TODO: Report this upstream

perl -i.orig -lpe 's/^(SHELL = \/bin\/sh).*/#$1/ and print "SHELL = /bin/bash"' makefile.in

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make

%install
rm -rf $RPM_BUILD_ROOT

make install     DESTDIR=$RPM_BUILD_ROOT
make install-man DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_std_includedir}
cd $RPM_BUILD_ROOT%{_std_includedir}
ln -s ../gnu/include/allegro.h .
ln -s ../gnu/include/allegro .

mkdir -p $RPM_BUILD_ROOT%{_std_bindir}
CONFLICTING_COMMANDS="
    :pack:
"

cd $RPM_BUILD_ROOT%{_bindir}
for f in *; do
    # don't symlink conflicting commands to /usr/bin
    echo $CONFLICTING_COMMANDS | grep ":${f}:" > /dev/null && continue
    ( cd $RPM_BUILD_ROOT%{_basedir}/bin; ln -s ../gnu/bin/$f . )
done

mkdir -p $RPM_BUILD_ROOT%{_std_libdir}
cd $RPM_BUILD_ROOT%{_std_libdir}
ln -s ../gnu/lib/liballeg* .

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_std_bindir}
%{_std_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_std_libdir}
%{_std_libdir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_std_includedir}
%{_std_includedir}/*.h
%{_std_includedir}/allegro
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%{_includedir}/allegro
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 4.2.2
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add copyright and grouping.
* Sat Oct 13 2007 - laca@sun.com
- add FOX build support
* Tue Mar 20 2007 - daymobrew@users.sourceforge.net
- Use single thread make so as not to break build.
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sat Jan  6 2007 - laca@sun.com
- make /usr/gnu compliant
* Wed Jan  3 2007 - laca@sun.com
- add SUNWxorg-headers dependency and add -I/usr/X11/include to CFLAGS
* Fri Jan 05 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Bump to 4.2.1.
* Tue Nov 14 2006 - Eric Boutilier
- Initial spec
