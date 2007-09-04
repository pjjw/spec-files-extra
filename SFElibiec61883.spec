#
# spec file for package SFElibiec61883
#
# includes module(s): libiec61883
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libiec6188364 = libiec61883.spec
%endif

%include base.inc
%use libiec61883 = libiec61883.spec

Name:		SFElibiec61883
Summary:	%{libiec61883.summary}
Version:	%{libiec61883.version}
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
%libiec6188364.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libiec61883.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libiec6188364.build -d %name-%version/%_arch64
%endif

%libiec61883.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libiec6188364.install -d %name-%version/%_arch64
%endif

%libiec61883.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/plugctl
%{_bindir}/plugreport
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/plugctl
%{_bindir}/%{_arch64}/plugreport
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
