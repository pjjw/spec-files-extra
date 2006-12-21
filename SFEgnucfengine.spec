#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEgnucfengine
Summary:             A tool for administering Networks of Diverse Machines
Version:             2.1.21
Source:              ftp://sunsite.uio.no/pub/cfengine/cfengine-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEbdb
BuildRequires: SFEbdb

Requires: SUNWopenssl-commands
BuildRequires: SUNWopenssl-commands
# The line above pretty much guarantees that the other SUNWopenssl*
# will be installed as well.

%prep
%setup -q -n cfengine-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --with-openssl="/usr/sfw" \
            --with-docs

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/cfengine
%{_datadir}/cfengine/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* 
* Thu Dec 21 2006 - Eric Boutilier
- Initial spec
