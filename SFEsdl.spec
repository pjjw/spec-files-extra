#
# spec file for package SFEsdl
#
# includes module(s): SDL
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define nasm_option --disable-nasm
%use sdl_64 = libsdl.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%define nasm_option --disable-nasm
%use sdl_sse2 = libsdl.spec
%endif

%include base.inc
%define nasm_option --disable-nasm
%use sdl = libsdl.spec

Name:                    SFEsdl
Summary:                 Simple DirectMedia - multimedia library
Version:                 1.2.11
Source:                  http://www.libsdl.org/release/SDL-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWxwrtl
Requires: SUNWxwplt
BuildConflicts: SUNWlibsdl

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%sdl_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%sdl_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%sdl.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%sdl_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.build -d %name-%version/%sse2_arch
%endif

%sdl.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%sdl_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.install -d %name-%version/%sse2_arch
%endif

%sdl.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sdl-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
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
* Sat Jul 14 2007 - dougs@truemail.co.th
- disable nasm
* Tue Jun  5 2007 - dougs@truemail.co.th
- Update to isabuild
* Thu Apr 26 2007 - dougs@truemail.co.th
- Added BuildConflicts: SUNWlibsdl
* Tue Sep 26 2006 - halton.huo@sun.com
- Bump version to 1.2.11
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEsdl
- change to root:bin to follow other JDS pkgs.
* Thu Apr 6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Wed Nov 09 2005 - glynn.foster@sun.com
- Initial spec
