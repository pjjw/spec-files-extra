#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                  SFErsync
Version:               2.6.8
Summary:               Rsync
Source:                http://samba.anu.edu.au/ftp/rsync/rsync-%{version}.tar.gz
BuildRoot:             %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:          %{_basedir}
%include default-depend.inc

%prep
%setup -q -n rsync-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS"                    \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Wed Nov 15 2006  <eric.boutilier@sun.com>
- Copied and transposed CBErsync to SFErsync
* Tue Aug 22 2006  <laca@sun.com>
- fix %files attributes
- move to /opt/jdsbld by default
* Wed Aug 16 2006  <laca@sun.com>
- add missing deps
- bump to 2.6.8
* Fri Sep 02 2005  <laca@sun.com>
- add man pages to %files
* Tue Jul 12 2005  <glynn.foster@sun.com>
- New CBE rsync package
