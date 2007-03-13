# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFExbindkeys
Summary:             An events grabbing program for X windows.
Version:             1.8.0
Source:              http://hocwp.free.fr/xbindkeys/xbindkeys-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Guarantee X/freetype environment, concisely (hopefully)
BuildRequires: SUNWxwplt 
Requires: SUNWxwplt 
BuildRequires: SFEguile
Requires: SFEguile

%prep
%setup -q -n xbindkeys-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointers"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --disable-tk         \
            --mandir=%{_mandir}

make -j$CPUS

# Uncomment this "in-line patch" and remove --disable-tk above if you want
# to enable the little tk script thingy (not worth in my opinion):

# perl -i.orig -lpe 's|^exec wish |exec /usr/sfw/bin/wish8.3 |' xbindkeys_show

# It corrects for the fact that wish is called wish8.3 and 
# lives in /usr/sfw/bin

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/xbindkeys*.1

%changelog
* 
* Mon Mar 05 2007 - Eric Boutilier
- Initial spec
