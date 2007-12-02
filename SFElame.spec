#
# spec file for package SFElame
#

%include Solaris.inc
Name:                    SFElame
Summary:                 LAME - A MP3 encoder
URL:                     http://lame.sourceforge.net/index.php
Version:                 3.97
Source:                  http://heanet.dl.sourceforge.net/sourceforge/lame/lame-%{version}.tar.gz
Patch1:                  lame-01-forte.diff
Patch2:                  lame-02-lines.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n lame-%version
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export LDFLAGS="-lX11"

./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Dec  2 2007 - laca@sun.com
- add patch 02 which renames a var called lines to lame_lines due to
  conflict with term.h(?)
* Thu Nov 16 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Initial spec
