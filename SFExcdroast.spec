#
# spec file for package SFExcdroast
#

%include Solaris.inc
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:                    SFExcdroast
Summary:                 X-CD-Roast - Flexible CD-burning software
URL:                     http://www.xcdroast.org/
Version:                 0.98alpha15
Source:                  http://switch.dl.sourceforge.net/sourceforge/xcdroast/xcdroast-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %option_with_gnu_iconv
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
BuildRequires: SFElibiconv-devel
Requires: SFEgettext
BuildRequires: SFEgettext-devel
%endif
%else
Requires: SUNWuiu8
%endif

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xcdroast-%version

%build
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl -lsocket"
%endif
export LDFLAGS="-lX11"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
	--enable-gtk2 \
	--sysconfdir=%{_sysconfdir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
[ -d $RPM_BUILD_ROOT%{_prefix}/etc ] && rmdir $RPM_BUILD_ROOT%{_prefix}/etc
[ -d $RPM_BUILD_ROOT%{_sysconfdir} ] && rmdir $RPM_BUILD_ROOT%{_sysconfdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_localedir}/locale.alias

%if %{build_l10n}
%else
rm -rf $RPM_BUILD_ROOT/%{_localedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_localedir}
%endif


%changelog
* Tue Jan 29 2008 - moinak.ghosh@sun.com
- Various fixes.
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Initial spec
