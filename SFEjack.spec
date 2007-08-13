#
# spec file for package jack
#
# includes module(s): jack
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use jack64 = jack.spec
%endif

%include base.inc
%use jack = jack.spec

Name:		SFEjack
Summary:	%{jack.summary}
Version:	%{jack.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFElibsndfile-devel
Requires:	SFElibsndfile
Requires:	oss

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
%jack64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%jack.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%jack64.build -d %name-%version/%_arch64
%endif

%jack.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%jack64.install -d %name-%version/%_arch64
%endif

%jack.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/jack*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/jack
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/jack*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/jack
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
* Mon Aug 13 2007 - dougs@truemail.co.th
- Added 64bit build
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
