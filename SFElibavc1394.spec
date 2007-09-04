#
# spec file for package SFElibavc1394
#
# includes module(s): libavc1394
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libavc139464 = libavc1394.spec
%endif

%include base.inc
%use libavc1394 = libavc1394.spec

Name:		SFElibavc1394
Summary:	%{libavc1394.summary}
Version:	%{libavc1394.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibraw1394-devel
Requires: SFElibraw1394

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
%libavc139464.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libavc1394.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libavc139464.build -d %name-%version/%_arch64
%endif

%libavc1394.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libavc139464.install -d %name-%version/%_arch64
%endif

%libavc1394.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dvcont
%{_bindir}/mkrfc2734
%{_bindir}/panelctl
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dvcont
%{_bindir}/%{_arch64}/mkrfc2734
%{_bindir}/%{_arch64}/panelctl
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
* Thu Sep  4 2007 - dougs@truemail.co.th
- Initial version
