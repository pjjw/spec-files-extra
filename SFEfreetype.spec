#
# spec file for package SFEfreetype
#
# includes module(s): freetype
#
%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use freetype_64 = freetype.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%use freetype_sse2 = freetype.spec
%endif

%include base.inc
%use freetype = freetype.spec

Name:                SFEfreetype
Summary:             Freetype
Version:             2.3.4
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWzlib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%freetype_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%freetype_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%freetype.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%freetype_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%freetype_sse2.build -d %name-%version/%sse2_arch
%endif

%freetype.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%freetype_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%freetype_sse2.install -d %name-%version/%sse2_arch
%endif

%freetype.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%if %arch_sse2
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%if %arch_sse2
%dir %attr (0755, root, bin) %{_bindir}/%{sse2_arch}
%{_bindir}/%{sse2_arch}/*
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif

%changelog
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial spec - some apps need modern freetype
