#
# spec file for package SFEgnome-device-manager
#
# includes module(s): gnome-device-manager
#

%include Solaris.inc
%use gdm = gnome-device-manager.spec

Name:                    SFEgnome-device-manager
Summary:                 GNOME Device Manager
Version:                 %{gdm.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-python-libs
BuildRequires: SUNWgnome-python-libs-devel
Requires: SUNWhal
BuildRequires: SUNWhal

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gdm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export LDFLAGS="%{_ldflags} -ldbus-glib-1 -L/usr/gnu/lib -R/usr/gnu/lib"
export CFLAGS="%optflags -I/usr/gnu/include"
%gdm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gdm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/gnome-device-manager
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/omf/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/gnome-device-manager/
%{_includedir}/gnome-device-manager/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Thu May 22 2008 - simon.zheng@sun.com
- Add copyright.
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version numbers.
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to search paths
* Fri Aug 31 2007 - simon.zheng@sun.com
- Gnome-device-manager is orignated from hal-device-manager,
  but it is written in C and able to manage device and driver.
* Wed Jun 06 2007 - nonsea@users.sourceforge.net
- Bump to 0.5.9.
- Remove patch hal-01-configure.diff.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Fixed configure.in typo
- Fixed non l10n build
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Rename sl_SI dir to sl in %install as sl_SI is a symlink to sl and causing
  installation problems as a dir.
* Wed Jan  3 2007 - laca@sun.com
- fix %{_datadir} attributes
* Wed Dec 13 2006 - jedy.wang@sun.com
- L10n support added.
* Mon Dec 11 2006 - jedy.wang@sun.com
- Initial spec
