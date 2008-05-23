#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use ncurses_64 = ncurses.spec
%endif

%include base.inc
%use ncurses = ncurses.spec

Name:                SFEncurses
Summary:             Emulation of SVR4 curses
Version:             5.6
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

export LDFLAGS="%_ldflags"
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%ncurses_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%ncurses.prep -d %name-%version/%{base_arch}

%build
if [ "x`basename $CC`" != xgcc ]
then
        FLAG64="-xarch=generic64"
else
        FLAG64="-m64"
fi

%ifarch amd64 sparcv9
export LDFLAGS="$FLAG64"
%ncurses_64.build -d %name-%version/%_arch64
%endif

export LDFLAGS=
%ncurses.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%ncurses_64.install -d %name-%version/%_arch64
# 64-bit binaries are of no benefit
rm -rf $RPM_BUILD_ROOT%{_bindir}/%_arch64
%endif

%ncurses.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5*
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7*
%dir %attr (0755, root, other) %{_datadir}/tabset
%{_datadir}/tabset/*
%dir %attr (0755, root, other) %{_datadir}/terminfo
%{_datadir}/terminfo/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Added proper 64-bit link flags to work with Sun Studio 11 and gcc
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 5.6.  Set LDFLAGS=-m64 for 64 bit build.
* Tue Mar 20 2007 - dougs@truemail.co.th
- Move build to a base spec. Added 64bit build
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
