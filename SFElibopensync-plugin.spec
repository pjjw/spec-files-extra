#
# spec file for package SFElibopensync-plugin
#
# includes module(s): libopensync-plugin-evo2
#                     libopensync-plugin-gcal
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use evo2 = libopensync-plugin-evo2.spec
%use gcal = libopensync-plugin-gcal.spec

Name:               SFElibopensync-plugin
Summary:            OpenSync - A data synchronization framework plugins
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Source1:           %{name}-manpages-0.1.tar.gz
Requires:           SFEswig
Requires:           SFEpylibs-httplib2
BuildRequires:      SFElibopensync-devel

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

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%evo2.build -d %name-%version
%gcal.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%evo2.install -d %name-%version
%gcal.install -d %name-%version

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
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
