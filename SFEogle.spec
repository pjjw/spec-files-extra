#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc


Name:                SFEogle
Summary:             Ogle DVD Player
Version:             0.9.2
Source:              http://www.dtek.chalmers.se/groups/dvd/dist/ogle-%{version}.tar.gz
URL:                 http://www.dtek.chalmers.se/groups/dvd/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibdvdcss-devel
BuildRequires: SFElibdvdread
BuildRequires: SFEliba52
Requires: SFElibdvdcss
Requires: SFElibdvdread
Requires: SFEliba52

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n ogle-%{version}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CFLAGS="-O4 -fno-omit-frame-pointer"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"

#export CFLAGS="%optflags"
#export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rmdir $RPM_BUILD_ROOT%{_bindir}
#rmdir $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Nov 21 2007 - daymobrew@users.sourceforge.net
- Initial spec
