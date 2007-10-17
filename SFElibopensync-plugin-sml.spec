#
# spec file for package SFElibopensync-plugin-sml
#
# includes module(s): libopensync-plugin-syncml
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner: halton
#

%include Solaris.inc
%use syncml = libopensync-plugin-syncml.spec

Name:               SFElibopensync-plugin-sml
Summary:            %{syncml}.summary
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SFElibopensync
Requires: SFElibsyncml
BuildRequires:      SFElibopensync-devel
BuildRequires:      SFElibsyncml-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version
%syncml.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%syncml.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%syncml.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/opensync
%dir %attr (0755, root, bin) %{_datadir}/opensync/defaults
%{_datadir}/opensync/defaults/syncml-http-server
%{_datadir}/opensync/defaults/syncml-obex-client

%changelog
* Wed Oct 17 2007 - nonsea@users.sourceforge.net
- Remove -devel pkg.
- Change %files
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Initial version.

