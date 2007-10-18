#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEeterm
Summary:             Terminal emulator intended as a replacement for xterm
Version:             0.9.4
Source:              http://%{sf_mirror}/sourceforge/eterm/Eterm-%{version}.tar.gz
Source2:			 http://www.eterm.org/download/Eterm-bg-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEimlib2
BuildRequires: SFElibast
Requires: SFEimlib2
Requires: SFElibast

%prep
%setup -q -n Eterm-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --enable-trans \
            --enable-static=no \
	    --disable-xim

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libEterm.la

cd ..
gtar fxvz %SOURCE2
cd bg
cp tile/* $RPM_BUILD_ROOT%{_datadir}/Eterm/pix/tile
cp scale/* $RPM_BUILD_ROOT%{_datadir}/Eterm/pix/scale

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, other) %{_datadir}/Eterm
%{_datadir}/Eterm/*

%changelog
* Thu Jan 28 2007 - mike kiedrowski (lakeside at cybrzn dot com)
- Added backgrounds package.
* Tue Nov 07 2006 - Eric Boutilier
- Initial spec
