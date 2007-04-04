#
# spec file for package SFElibopensync-plugin
#
# includes module(s): libopensync-plugin-evo2
#                     libopensync-plugin-gcal
#                     libopensync-plugin-file
#                     libopensync-plugin-palm
#                     libopensync-plugin-syncml
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define with_pilot_link %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use evo2 = libopensync-plugin-evo2.spec
%use gcal = libopensync-plugin-gcal.spec
%use file = libopensync-plugin-file.spec
%if %with_pilot_link
%use palm = libopensync-plugin-palm.spec
  %define plink_prefix /usr
%endif
%use syncml = libopensync-plugin-syncml.spec

Name:               SFElibopensync-plugin
Summary:            OpenSync - A data synchronization framework plugins
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWevolution-data-server
Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SFEswig
Requires: SFElibopensync
Requires: SFEpylibs-httplib2
%if %with_pilot_link
  Requires:         SUNWpilot-link
  BuildRequires:    SUNWpilot-link-devel
%endif
Requires:           SFEwbxml
Requires:           SFElibsyncml
BuildRequires:      SFElibopensync-devel
BuildRequires:      SFElibsyncml-devel
Requires:           SFEopenobex
BuildRequires:      SFEopenobex-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%evo2.prep -d %name-%version
%gcal.prep -d %name-%version
%file.prep -d %name-%version
%if %with_pilot_link
  %palm.prep -d %name-%version
%endif
%syncml.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%if %with_pilot_link
  export CFLAGS="-I%{_includedir} %optflags -I%{plink_prefix}/include/libpisock"
  export LDFLAGS="-L%{_libdir} -R%{_libdir} -L%{plink_prefix}/lib -R%{plink_prefix}/lib"
%else
  export CFLAGS="-I%{_includedir} %optflags"
  export LDFLAGS="-L%{_libdir} -R%{_libdir}"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%evo2.build -d %name-%version
%gcal.build -d %name-%version
%file.build -d %name-%version
%if %with_pilot_link
  %palm.build -d %name-%version
%endif
%syncml.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%evo2.install -d %name-%version
%gcal.install -d %name-%version
%file.install -d %name-%version
%if %with_pilot_link
  %palm.install -d %name-%version
%endif
%syncml.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/opensync

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr  3 2007 - laca@sun.com
- add openobex dependency
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
- Change plink_prefix from /usr/sfw to /usr
* Fri Jan 11 2007 - jijun.yu@sun.com
- Add new plugin: syncml
* Fri Nov 17 2006 - halton.huo@sun.com
- Add new plugin: file and palm
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
