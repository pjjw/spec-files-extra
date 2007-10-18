#
# spec file for package SFElibopensync-plugin-palm
#
# includes module(s): libopensync-plugin-palm
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
# 

%include Solaris.inc
%use palm = libopensync-plugin-palm.spec

Name:               SFElibopensync-plugin-palm
Summary:            %palm.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWpilot-link
Requires: SFElibopensync
BuildRequires:    SUNWpilot-link-devel
BuildRequires:    SFElibopensync-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%palm.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags -I%{_includedir}/libpisock"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%palm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%palm.install -d %name-%version

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
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Remove useless with_pilot_link logic
* Mon Aug 06 2007 - jijun.yu@sun.com
- Splitted from SFElibopensync-plugin.spec.
- Bump to 0.32.

