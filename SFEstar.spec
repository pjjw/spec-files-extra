# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define tarball_version 1.5a75

# Relegating to /usr/gnu to avoid name collisions...
%define _prefix %{_basedir}/gnu

Name:                SFEstar
Summary:             fast POSIX-compliant tar
Version:             1.5
Source:              ftp://ftp.berlios.de/pub/star/alpha/star-%{tarball_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n star-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

/usr/ccs/bin/make

%install

export INS_BASE=$RPM_BUILD_ROOT%{_prefix}
export MANDIR=share/man
export DEFUMASK=022

rm -rf $RPM_BUILD_ROOT

/usr/ccs/bin/make -e install

rm -rf ${RPM_BUILD_ROOT}%{_libdir}
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/etc
rm -rf ${RPM_BUILD_ROOT}%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*

%changelog
* 
* Wed Nov 15 2006 - Eric Boutilier
- Initial spec
