#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEaxyftp
Summary:             Graphical ftp client
Version:             0.5.1
Source:              http://www.wxftp.seul.org/download/axyftp-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWdtbas
Requires: SUNWmfrun
Requires: SUNWxwice
Requires: SUNWxwplt

%prep
%setup -q -n axyftp-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -R/usr/dt/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rmdir ${RPM_BUILD_ROOT}%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Sat Oct 14 2006 - laca@sun.com
- disable parallel build as it breaks on multicpu systems
* Mon Sep 25 2006 - Eric Boutilier
- Initial spec
