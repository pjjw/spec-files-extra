#
# spec file for package SFEelectric-fence
#
# includes module(s): electric-fence
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use efence64 = electric-fence.spec
%endif

%include base.inc
%use efence = electric-fence.spec

Name:		SFEelectric-fence
Summary:	%{efence.summary}
Version:	%{efence.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%efence64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%efence.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%efence64.build -d %name-%version/%_arch64
%endif

%efence.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%efence64.install -d %name-%version/%_arch64
%endif

%efence.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial spec
