#
# spec file for package SFElibraw1394
#
# includes module(s): libraw1394
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libraw139464 = libraw1394.spec
%endif

%include base.inc
%use libraw1394 = libraw1394.spec

Name:		SFElibraw1394
Summary:	%{libraw1394.summary}
Version:	%{libraw1394.version}
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
%libraw139464.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libraw1394.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libraw139464.build -d %name-%version/%_arch64
%endif

%libraw1394.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libraw139464.install -d %name-%version/%_arch64
%endif

%libraw1394.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dumpiso
%{_bindir}/sendiso
%{_bindir}/testlibraw
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dumpiso
%{_bindir}/%{_arch64}/sendiso
%{_bindir}/%{_arch64}/testlibraw
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
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial version
