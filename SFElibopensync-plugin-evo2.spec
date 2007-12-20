#
# spec file for package SFElibopensync-plugin-evo2
#
# includes module(s): libopensync-plugin-evo2
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
#

%include Solaris.inc
%use evo2 = libopensync-plugin-evo2.spec

Name:               SFElibopensync-plugin-evo2
Summary:            %evo2.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWevolution-data-server
Requires: SUNWgnome-base-libs
Requires: SFElibopensync
BuildRequires:      SFElibopensync-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version
%evo2.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%evo2.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%evo2.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/opensync-1.0

%changelog
* Thu Dec 20 2007 - jijun.yu@sun.coom
- Change %{_datadir}/opensync to %{_datadir}/opensync-1.0
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Remove -devel package since there is no header files.
* Mon Aug 06 2007 - jijun.yu@sun.com
- Splitted from SFElibopensync-plugin.spec
- Bump to 0.32

