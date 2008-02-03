#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEprtpci
License:             CDDL
Summary:             A tool for summarizing PCI information from prtconf output
Version:             1.11
Patch1:              prtpci-01-etc.diff

URL:                 http://blogs.sun.com/dmick/entry/prtpci_digest_and_display_prtconf
Source:              ftp://playground.sun.com/pub/dmick/prtpci.tar.Z
Source1:             http://pciids.sourceforge.net/pci.ids

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc
Requires: SUNWcsr

%prep
cd ${RPM_BUILD_DIR}
rm -rf prtpci
mkdir prtpci
cd prtpci
uncompress -c %{SOURCE} | tar xvf - 
%patch1 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT

cd prtpci
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/pciids

cp prtpci ${RPM_BUILD_ROOT}%{_bindir}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/prtpci
(cd ${RPM_BUILD_ROOT}%{_bindir}
    ln -s prtpci lspci)
cp pciids/* ${RPM_BUILD_ROOT}%{_sysconfdir}/pciids
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/pciids/pci.ids

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Mon Feb 04 2008 - moinak.ghosh@sun.com
- Initial spec.
