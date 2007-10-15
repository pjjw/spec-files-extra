#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEw3m
Summary:             A text-based web browser
Version:             0.5.2
URL:                 http://w3m.sourceforge.net/
Source:              http://superb-west.dl.sourceforge.net/sourceforge/w3m/w3m-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
Requires:            SUNWlibmsr
Requires:            SUNWperl584core
Requires:            SUNWxwrtl
Requires:            SUNWzlib
Requires:            SFEbdw-gc
Requires:            SUNWopenssl-libraries
BuildRequires:       SUNWgnome-base-libs-devel
BuildRequires:       SUNWopenssl-include
BuildRequires:       SFEbdw-gc-devel

%prep
%setup -q -n w3m-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -lX11 -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  		\
			--libexecdir=%{_libdir}		\
			--mandir=%{_mandir} 		\
			--enable-static=no			\
			--with-browser=/usr/bin/firefox

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/w3m/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/ja/man*/*
%{_mandir}/man*/*

%changelog
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Add URL
* Tue Sep 11 2007 - nonsea@users.sourceforge.net
- Add --with-browser=/usr/bin/firefox, replace default value mozilla.
* Wed Sep 05 2007 - nonsea@users.sourceforge.net
- Bump to 0.5.2
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Initial spec
