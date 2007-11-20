#
# spec file for package SFEaria
#
# includes module(s): aria2
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use aria2 = aria2.spec

Name:               SFEaria
Summary:            aria2 - A download utility with resuming and segmented downloading
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnutls
Requires: SUNWlibC
Requires: SUNWlibgcrypt
Requires: SUNWlibgpg-error
Requires: SUNWlibmsr


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
%aria2.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export CXXFLAGS="-lsocket  -lnsl"
export RPM_OPT_FLAGS="$CFLAGS"
%aria2.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%aria2.install -d %name-%version

rm $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -r $RPM_BUILD_ROOT%{_libdir}

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
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Dec 19 2006 - halton.huo@sun.com
- initial version created
