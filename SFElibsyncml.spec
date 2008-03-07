#
# spec file for package SFElibsyncml
#
# includes module(s): libsyncml
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%include Solaris.inc

%use libsyncml = libsyncml.spec

Name:               SFElibsyncml
Summary:            libsyncml - C library implementation of the SyncML protocol
Version:            %{libsyncml.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWevolution-libs
Requires:      SFEopenobex
Requires:      SFEwbxml
BuildRequires: SFEcmake
BuildRequires: SUNWevolution-libs-devel
BuildRequires: SFEopenobex-devel
BuildRequires: SFEwbxml-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}

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
%libsyncml.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-g"
#export CFLAGS="%optflags -g"
#export LD_LIBRARY_PATH="-L /usr/sfw/lib -R /usr/sfw/lib"
export CXXFLAGS="-lsocket  -lnsl"
export RPM_OPT_FLAGS="$CFLAGS"
%libsyncml.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libsyncml.install -d %name-%version

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Mar 07 2008 - nonsea@users.sourceforge.net
- Update %files caused by upgrading.
* Fri Oct 19 2007 - jijun.yu@sun.com
- Remove the optimum cflags.
* Wed Oct 17 2007 - nonsea@users.sourceforge.net
- Add SUNWevolution-libs to Requires, add SUNWevolution-libs-devel
  to BuildRequires, because libsyncml using libsoup
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Add SFEwbxml to Requires, add SFEwbxml-devel to BuildRequires
* Fri Sept 21 2007 - jijun.yu@sun.com
- add debug flags.
* Tue Apr  3 2007 - laca@sun.com
- add openobex dependency
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add attr (0755, root, sys) %{_datadir}
* Thu Jan 11 2006 - jijun.yu@sun.com
- initial version created
