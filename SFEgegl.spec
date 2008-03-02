#
# spec file for package SFEgegl
#
# includes module(s): gegl
#
%include Solaris.inc
%use gegl = gegl.spec

Name:                    SFEgegl
Summary:                 GEGL (Generic Graphics Library) is a graph based image processing framework.
Version:                 %{gegl.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgnome-libs
BuildRequires:           SUNWgnome-libs-devel
Requires:		 SFEbabl
BuildRequires:           SFEbabl-devel

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
%gegl.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
%gegl.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gegl.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

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
%dir %attr (0755, root, bin) %{_libdir}/gegl-1.0
%{_libdir}/gegl-1.0/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/gegl-1.0
%{_includedir}/gegl-1.0/*.h
%dir %attr (0755, root, bin) %{_includedir}/gegl-1.0/gegl
%{_includedir}/gegl-1.0/gegl/*.h
%dir %attr (0755, root, bin) %{_includedir}/gegl-1.0/gegl/buffer
%{_includedir}/gegl-1.0/gegl/buffer/*.h
%dir %attr (0755, root, bin) %{_includedir}/gegl-1.0/gegl/property-types
%{_includedir}/gegl-1.0/gegl/property-types/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html/gegl
%{_datadir}/gtk-doc/html/gegl/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version numbers.
* Fri Dec 14 2007 - simon.zheng@sun.com
- Create
