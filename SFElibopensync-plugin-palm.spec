#
# spec file for package SFElibopensync-plugin-palm
#
# includes module(s): libopensync-plugin-palm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
# 

%include Solaris.inc
%use palm = libopensync-plugin-palm.spec

Name:               SFElibopensync-plugin-palm
Summary:            %palm.summary
Version:            %{palm.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWpilot-link
Requires: SFElibopensync
BuildRequires:    SUNWpilot-link-devel
BuildRequires:    SFElibopensync-devel

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
%{_datadir}/opensync-1.0

%changelog
* Thu Dec 20 2007 - jijun.yu@sun.com
- Change %{_datadir}/opensync to %{_datadir}/opensync-1.0
- Remove -devel package
* Tue Oct 16 2007 - nonsea@users.sourceforge.net
- Remove useless with_pilot_link logic
* Mon Aug 06 2007 - jijun.yu@sun.com
- Splitted from SFElibopensync-plugin.spec.
- Bump to 0.32.

