#
# spec file for package SFEgftp
#

%include Solaris.inc
Name:                    SFEgftp
Summary:                 gFTP - Multithreaded FTP client for Unix based machines
URL:                     http://gftp.seul.org/
Version:                 2.0.18
Source:                  http://gftp.seul.org/gftp-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
# date:2008-09-23 owner:alfred type:up-streamed
Patch1:                  gftp-01-solaris-in-trunk.diff

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gftp-%version
%patch1 -p1

%build
export LDFLAGS="-lX11"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif

#TODO: check --disable-sm 
CC=$CC CXX=$CXX CFLAGS="$CFLAGS" ./configure --prefix=%{_prefix} \
            --mandir=%{_prefix}/share/man --disable-sm
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %{build_l10n}
%else
rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gftp
%{_datadir}/gftp/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Sep 28 2008 - alfred.peng@sun.com
- Update group bit for %{_datadir}/man.
* Wed Sep 24 2008 - alfred.peng@sun.com
- Backport the patch gftp-01-solaris-in-trunk.diff from trunk to build
  with Sun Studio.
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
