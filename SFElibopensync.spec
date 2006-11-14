#
# spec file for package SFElibopensync
#
# includes module(s): libopensync
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use libopensync = libopensync.spec

Name:               SFElibopensync
Summary:            OpenSync - libopensync - A data synchronization framework
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Source1:           %{name}-manpages-0.1.tar.gz
Requires:           SFEsqlite
Requires:           SFEswig
BuildRequires:      SFEsqlite-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libopensync.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
#PYTHON_VERSION=`python -V 2>&1 | awk '{print $2}' | awk -F\. '{print $1"."$2}'`
#export PYTHON_VERSION
%libopensync.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libopensync.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python2.4
%{_libdir}/opensync
%{_libdir}/osplugin
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
