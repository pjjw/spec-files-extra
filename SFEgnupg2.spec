#
# spec file for package SFEgnupg
#
# includes module(s): gnupg
#
#

%include Solaris.inc
%use gnupg = gnupg2.spec

Name:          SFEgnup2
Summary:       %{gnupg.summary}
Version:       %{gnupg.version}
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWbzip
Requires: SUNWzlib

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gnupg.prep -d %name-%version

%build
export CFLAGS="%optflags"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags -lsocket"
%gnupg.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnupg.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnupg
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (0755, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Dec 29 2007 - jijun.yu@sun.com
- initial version created
