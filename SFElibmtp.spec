#
# spec file for package SFElibmtp
#
# includes module(s): libmtp
#
%include Solaris.inc
# The is no 64bit libusb :(

%use libmtp = libmtp.spec

%define SFEdoxygen      %(/usr/bin/pkginfo -q SFEdoxygen && echo 1 || echo 0)

Name:		SFElibmtp
Summary:	%{libmtp.summary}
Version:	%{libmtp.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%if %SFEdoxygen
%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%libmtp.prep -d %name-%version/%{base_arch}

%build
%libmtp.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%libmtp.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mtp-*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %SFEdoxygen
%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%endif

%changelog
* Tue Sep 18 2007 - dougs@truemail.co.th
- Initial version
