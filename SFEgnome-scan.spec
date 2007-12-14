#
# spec file for package SFEgnome-scan
#
# includes module(s): gnome-scan
#
%include Solaris.inc
%use gs = gnome-scan.spec

Name:                    SFEgnome-scan
Summary:                 Scanner client for the GNOME desktop
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgnome-libs
BuildRequires:           SUNWgnome-libs-devel
Requires:                SFEsane-backends
BuildRequires:           SFEsane-backends-devel
Requires:		 SFEgegl
BuildRequires:		 SFEgegl-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-libs-devel
Requires: SFEsane-backends-devel

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
%gs.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
%gs.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gs.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Remove doc
rm -fr $RPM_BUILD_ROOT/usr/doc

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gimp
%dir %attr (0755, root, bin) %{_libdir}/gnome-scan-1.0
%{_libdir}/gnome-scan-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome-scan
%dir %attr (0755, root, other) %{_datadir}/gnome-scan/icons
%dir %attr (0755, root, other) %{_datadir}/gnome-scan/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/gnome-scan/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/gnome-scan/icons/hicolor/scalable/actions
%{_datadir}/gnome-scan/icons/hicolor/scalable/actions/*
%dir %attr (0755, root, other) %{_datadir}/icons/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%{_datadir}/icons/hicolor/scalable/apps/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Dec 14 2007 - simon.zheng@sun.com
- Rename SFEgnomescan.spec as SFEgnome-scan.spec.
  Add dependency on SFEgegl.

* Tue Mar 20 2007 - simon.zheng@sun.com
- Split into 2 files, SFEgnomescan.spec and
  linux-specs/gnomescane.spec

* Wed Mar  1 2007 - simon.zheng@sun.com
- Bump to 0.4.0.4.
- Rework patch gnomescan-01-build.diff.

* Wed Nov  8 2006 - laca@sun.com
- Create
