#
# spec file for package SFEy4mscaler
#
# includes module(s): y4mscaler
#
%include Solaris.inc
%use y4mscaler = y4mscaler.spec

Name:		SFEy4mscaler
Summary:	%{y4mscaler.summary}
Version:	%{y4mscaler.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEmjpegtools-devel
Requires: SFEmjpegtools

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%y4mscaler.prep -d %name-%version/%{base_arch}

%build
%y4mscaler.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%y4mscaler.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Wed Sep  5 2007 - dougs@truemail.co.th
- Initial version
