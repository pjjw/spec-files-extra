#
# spec file for package SFEstdcxx
#
# includes module(s): stdcxx
#
%include Solaris.inc

%define gnu_prefix gnu/stdcxx
%define sunpro_prefix stdcxx

%ifarch amd64 sparcv9
%include arch64.inc
%use stdcxx64 = stdcxx.spec
%endif

%include base.inc
%use stdcxx = stdcxx.spec

Name:		SFEstdcxx
Summary:	%{stdcxx.summary}
Version:	%{stdcxx.version}
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
%stdcxx64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%stdcxx.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%stdcxx64.build -d %name-%version/%_arch64
%endif

%stdcxx.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%stdcxx64.install -d %name-%version/%_arch64
%endif

%stdcxx.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_prefix}/%{sunpro_prefix}/lib
%{_prefix}/%{gnu_prefix}/lib

%files devel
%defattr (-, root, bin)
%{_prefix}/%{sunpro_prefix}/include
%{_prefix}/%{gnu_prefix}/include

%changelog
* Wed May  7 2008 - cypromis@opensolaris.org
- upgraded to 4.2.1
- some minor changes for SPARC compliance
* Wed Sep  5 2007 - dougs@truemail.co.th
- Initial version
