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
%define with_pilot_link %(pkginfo -q SUNWhal && echo 1 || echo 0)

%if %with_pilot_link
%use palm = libopensync-plugin-palm.spec
  %define plink_prefix /usr
%endif

Name:               SFElibopensync-plugin-palm
Summary:            OpenSync - A data synchronization framework plugins
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SFEswig
Requires: SFElibopensync
%if %with_pilot_link
  Requires:         SUNWpilot-link
  BuildRequires:    SUNWpilot-link-devel
%endif
BuildRequires:      SFElibopensync-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%if %with_pilot_link
  %palm.prep -d %name-%version
%endif

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
%if %with_pilot_link
  %palm.build -d %name-%version
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %with_pilot_link
  %palm.install -d %name-%version
%endif

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
* Mon Aug 06 2007 - jijun.yu@sun.com
- Splitted from SFElibopensync-plugin.spec.
- Bump to 0.32.

