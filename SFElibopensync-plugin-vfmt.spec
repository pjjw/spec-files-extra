#
# spec file for package SFElibopensync-plugin-vfmt
#
# includes module(s): libopensync-plugin-vformat
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
#

%include Solaris.inc
%use vformat = libopensync-plugin-vfmt.spec

Name:               SFElibopensync-plugin-vfmt
Summary:            OpenSync - A data synchronization framework plugins
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SFEswig
Requires: SFElibopensync
BuildRequires:      SFElibopensync-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%vformat.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%vformat.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%vformat.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Mon Aug 06 2007 - jijun.yu@sun.com
- Initial version.

