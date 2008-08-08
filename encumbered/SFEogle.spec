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
Patch1:              ogle-01-mmx.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibdvdcss-devel
BuildRequires: SFElibdvdnav
BuildRequires: SFEliba52
Requires: SFElibdvdcss
Requires: SFElibdvdnav
Requires: SFEliba52

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n ogle-%{version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CFLAGS="-O4 -fno-omit-frame-pointer -I/usr/X11/include"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"

#export CFLAGS="%optflags"
#export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir}
rm -f $RPM_BUILD_ROOT%{_libdir}/ogle/lib*a
(cd ogle/.libs/; cp -rP libdvdcontrol.so* $RPM_BUILD_ROOT%{_libdir}/ogle/)
mv $RPM_BUILD_ROOT%{_libdir}/ogle/libdvdcontrol.so.9.2.0U $RPM_BUILD_ROOT%{_libdir}/ogle/libdvdcontrol.so.9.2.0

#rmdir $RPM_BUILD_ROOT%{_bindir}
#rmdir $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/ogle
%{_datadir}/ogle/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Rename SFElibdvdread dependency to SFElibdvdnav
* Sun Jan 21 2008 - moinak.ghosh@sun.com
- Fixed ogle build to include libdvdcontrol, add missing dirs to package
- Patch to fix MediaLib and MMX usage
* Wed Nov 21 2007 - daymobrew@users.sourceforge.net
- Initial spec
