#
# spec file for package SFEopenexr.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define apache2_vers 2.2

Name:                   SFEhtdig
Summary:                HTML Indexing and Search engine
Version:                3.2.0b6
Source:                 %{sf_download}/files/htdig-%{version}.tar.gz
URL:                    http://www.htdig.org/
Patch1:                 htdig-01-debian.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc
Requires: SUNWzlib
BuildRequires: SUNWzlib

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires:               %{name}
%include default-depend.inc

%prep
%setup -q -n htdig-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -lintl -liconv"
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --localstatedir=%{_localstatedir} \
            --with-database-dir=%{_localstatedir}/htdig \
            --enable-shared=yes		\
	    --enable-static=no		\
            --without-apache		\
            --with-pic			\
            --with-cgi-bin-dir=%{_localstatedir}/apache2/%{apache2_vers}/cgi-bin \
            --with-search-dir=%{_datadir}/htdocs/htdig \
            --with-image-dir=%{_datadir}/htdocs/htdig \
            --with-config-dir=%{_sysconfdir}/htdig


make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.*la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/htdocs
%{_datadir}/htdocs/*
%dir %attr (0755, root, other) %{_datadir}/htdig
%{_datadir}/htdig/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/htdig

%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_localstatedir}
%{_localstatedir}/apache2
%attr (0755, root, bin) %dir %{_localstatedir}/htdig

%changelog
* Fri Feb 01 2008 - moinak.ghosh@sun.com
- Added jumbo patch from Debian Etch (several improvemements) with
- further additions to fix Makefile issues causing undefined symbols
- at runtime.
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Initial spec.
