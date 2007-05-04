#
# spec file for package SFExosd
#

%include Solaris.inc
Name:                    SFExosd
Summary:                 xosd - simple library to display shaped text on X Display
URL:                     http://freshmeat.net/redir/xosd/12072/url_homepage/libxosd
Version:                 2.2.14
Source:                  http://freshmeat.net/redir/xosd/12072/url_tgz/xosd-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n xosd-%version

%build

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#empty directories (xmms):
rm -r $RPM_BUILD_ROOT/opt

rm -r $RPM_BUILD_ROOT/%{_libdir}/*la

%if %build_l10n
#TODO check if needed  # Rename pl_PL dir to pl as pl_PL is a symlink to pl and causing installation
#TODO check if needed  # problems as a dir.
#TODO check if needed  cd $RPM_BUILD_ROOT%{_datadir}/locale
#TODO check if needed  mv pl_PL pl
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/xosd
%{_datadir}/xosd/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Thu Apr 07 2007  - Thomas Wagner
- Initial spec