#
# spec file for package SFEdvgrab
#
# includes module(s): dvgrab
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use dvgrab64 = dvgrab.spec
%endif

%include base.inc
%use dvgrab = dvgrab.spec

Name:		SFEdvgrab
Summary:	%{dvgrab.summary}
Version:	%{dvgrab.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibiec61883-devel
Requires: SFElibiec61883
BuildRequires: SFElibraw1394-devel
Requires: SFElibraw1394
BuildRequires: SFElibdv-devel
Requires: SFElibdv
BuildRequires: SFElibquicktime-devel
Requires: SFElibquicktime

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%dvgrab64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%dvgrab.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%dvgrab64.build -d %name-%version/%_arch64
%endif

%dvgrab.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%dvgrab64.install -d %name-%version/%_arch64
%endif

%dvgrab.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dvgrab
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dvgrab
%endif

%changelog
* Thu Sep  4 2007 - dougs@truemail.co.th
- Added libquicktime as required
* Thu Sep  4 2007 - dougs@truemail.co.th
- Initial version
