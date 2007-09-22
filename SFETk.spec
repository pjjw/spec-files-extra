#
# spec file for package SFETk
#
# includes module(s): Tk
# Only build missing 64bit Tk
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use Tk = Tk.spec
%endif

%include base.inc

Name:		SFETk
Summary:	%{Tk.summary}
Version:	%{Tk.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%Tk.prep -d %name-%version/%_arch64
%endif

%build
%ifarch amd64 sparcv9
%Tk.build -d %name-%version/%_arch64
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%Tk.install -d %name-%version/%_arch64
%endif
# Remove everything already installed from SUNWTk
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/tk8.4
rm -rf $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.a
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/tkConfig.sh
%{_libdir}/%{_arch64}/tk8.4
%endif

%changelog
* Sat Sep 22 2007 - dougs@truemail.co.th
- Initial version
