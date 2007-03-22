#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEworker
Summary:             A highly configurable graphical file manager for X
Version:             2.14.1
Source:              http://www.boomerangsworld.de/cms/worker/downloads/worker-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Guarantee X environment, concisely (hopefully)
BuildRequires: SUNWxwplt 
Requires: SUNWxwplt 
Requires: SUNWgccruntime

BuildRequires: SFEavfs-devel
Requires: SFEavfs

%prep
%setup -q -n worker-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

# Apparently sed usage in this source is GNU-specific, so
# the following forces GNU sed to be used:
export PATH=/usr/gnu/bin:$PATH

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/worker
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/worker
%{_datadir}/worker/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Thu Mark 22 2007 - daymobrew@users.sourceforge.net
- Fix perms for pixmaps dir.
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Mon Mar 12 2007 - Eric Boutilier
- Initial spec
