#
# spec file for package SFEalsa-plugins
#
# includes module(s): alsa-plugins
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use alsa64 = alsa-plugins.spec
%endif

%include base.inc
%use alsa = alsa-plugins.spec

Name:                    SFEalsa-plugins
Summary:                 %{alsa.summary}
Version:                 %{alsa.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: oss
BuildRequires: SUNWdbus-devel
Requires: SUNWdbus
BuildRequires: SFEalsa-lib-devel
Requires: SFEalsa-lib
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%alsa64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%alsa.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%alsa64.build -d %name-%version/%_arch64
%endif

%alsa.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%alsa64.install -d %name-%version/%_arch64
%endif

%alsa.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%config %{_sysconfdir}/asound.conf

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
