#
# spec file for package SFElibopensync-plugin-file
#
# includes module(s): libopensync-plugin-file
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner jerryyu
#

%include Solaris.inc
%use file = libopensync-plugin-file.spec

Name:               SFElibopensync-plugin-file
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
%file.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%file.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%file.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/opensync

%changelog
* Wed Jun 05 2007 - jijun.yu@sun.com
- Splitted from SFElibopensync-plugin.spec and bumped to 0.30

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
