#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEckermit
Summary:             Serial and network communication / file transfer program
Version:             8.0.211
Source:              ftp://kermit.columbia.edu/kermit/archives/cku211.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -c -n kermit-%{version}

%build

# EM conflicts with an openssl type
perl -pi~ -e s/EM/EM_/ ckcasc.h

make solaris9g+openssl+zlib+pam+shadow

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}/kermit
install -d -m 0755 $RPM_BUILD_ROOT/%{_mandir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_mandir}/man1

install -m 0755 wermit $RPM_BUILD_ROOT/%{_bindir}/kermit
install -m 0644 ckuker.nr $RPM_BUILD_ROOT/%{_mandir}/man1/kermit.1

for f in COPYING.TXT ckcbwr.txt ckubwr.txt ckuins.txt ckccfg.txt \
	 ckcplm.txt ckermit.ini ckermod.ini ckermit70.txt ckermit80.txt; do
  install -m 0644 $f $RPM_BUILD_ROOT/%{_docdir}/kermit
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/kermit
%{_docdir}/kermit/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1

%changelog
* Fri Jun 06 2008 - river@wikimedia.org
- fix modes on docdir
* Tue May 1 2008 - river@wikimedia.org
- Initial spec
