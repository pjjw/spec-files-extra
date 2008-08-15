#
# spec file for package SFEadns
#
# includes module(s): adns
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use adns64 = adns.spec
%endif

%include base.inc
%use adns = adns.spec

Name:                    SFEadns
Summary:                 %{adns.summary}
Version:                 %{adns.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 %{name}.copyright
Group:			 Network
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - Development Files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%adns64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%adns.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%adns64.build -d %name-%version/%_arch64
%endif

%adns.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%adns64.install -d %name-%version/%_arch64
rm -rf $RPM_BUILD_ROOT%{_bindir}
%endif

%adns.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/adns*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add license and grouping
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial version
