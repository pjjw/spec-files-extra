#
# spec file for package SFElibdv
#
# includes module(s): libdv
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libdv64 = libdv.spec
%endif

%include base.inc
%use libdv = libdv.spec

Name:		SFElibdv
Summary:	%{libdv.summary}
Version:	%{libdv.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libdv64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libdv.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libdv64.build -d %name-%version/%_arch64
%endif

%libdv.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libdv64.install -d %name-%version/%_arch64
%endif

%libdv.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dubdv
%{_bindir}/dvconnect
%{_bindir}/encodedv
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dubdv
%{_bindir}/%{_arch64}/dvconnect
%{_bindir}/%{_arch64}/encodedv
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Thu Aug 30 2007 - dougs@truemail.co.th
- Initial version
