#
# spec file for package SFEgrip
#

%include Solaris.inc
Name:                    SFEgrip
Summary:                 Cd-player and cd-ripper for the Gnome desktop
URL:                     http://nostatic.org/grip/
Version:                 3.3.1
Source:                  http://prdownloads.sourceforge.net/grip/grip-%{version}.tar.gz
Patch1:			 grip-01-i386.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:		 SFEcurl

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n grip-%version
%patch1 -p1

%build
export LDFLAGS="-lX11"
./configure --prefix=%{_prefix} --disable-shared-cdpar --disable-shared-id3
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#move locale to /usr/share
mv $RPM_BUILD_ROOT%{_libdir}/locale $RPM_BUILD_ROOT%{_datadir}/
rmdir $RPM_BUILD_ROOT%{_libdir}

%if %build_l10n
# Rename pl_PL dir to pl as pl_PL is a symlink to pl and causing installation
# problems as a dir.
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv pl_PL pl
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
%{_bindir}/grip
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/grip.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/grip
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/gripicon.png
%{_datadir}/pixmaps/griptray.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Rename pl_PL dir to pl in %install as pl_PL is a symlink to pl and causing
  installation problems as a dir.

* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Correct %files perms and add l10n package for l10n.

* Fri Mar 16 2007  - irene.huang@sun.com
- created
