#
# spec file for package SFEeclipse
#
# includes module(s): eclipse
#
%include Solaris.inc

%include base.inc
%use eclipse = eclipse.spec

Name:		SFEeclipse
Summary:	%{eclipse.summary}
Version:	%{eclipse.version}
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

mkdir %name-%version/%{base_arch}
%eclipse.prep -d %name-%version/%{base_arch}

%build
%eclipse.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%eclipse.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr(755,root,bin) %{_bindir}/eclipse
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/eclipse
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/eclipse

%changelog
* Sat Sep  8 2007 - dougs@truemail.co.th
- Initial version
