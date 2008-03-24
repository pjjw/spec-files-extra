#
# spec file for package SFEqterm
#
# includes module(s): qterm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: Halton
#

%include Solaris.inc

%use qterm = qterm.spec

Name:               SFEqterm
Summary:            qterm - 
Version:            %{qterm.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgccruntime
Requires:      SFEqt
BuildRequires: SFEcmake
BuildRequires: SFEqt-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%qterm.prep -d %name-%version

%build
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
%qterm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%qterm.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qterm

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Mar 24 2008 - nonsea@users.sourceforge.net
- initial version created
