#
# spec file for package SFEopenexr.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                   SFEgnokii
Summary:                Tools and user-space drivers for interfacing with mobiles phones esp. Nokia
Version:                0.6.22
Source:                 http://www.gnokii.org/download/gnokii/gnokii-0.6.22.tar.bz2
Patch1:                 gnokii-01-uint8.diff
Patch2:                 gnokii-02-utils.diff
Patch3:                 gnokii-03-makefile.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibical
BuildRequires: SFElibical-devel
Requires: SFEgettext
BuildRequires: SFEgettext-devel
Requires: SFElibiconv
BuildRequires: SFElibiconv-devel

%prep
%setup -q -n gnokii-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
            --enable-shared=yes		\
	    --enable-static=no		\
            --with-libiconv-prefix=/usr/gnu \
            --with-libintl-prefix=/usr/gnu


make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a
mv $RPM_BUILD_ROOT/%{_prefix}/man/man1/xgnokii.1x $RPM_BUILD_ROOT/%{_mandir}/man1/
rm -rf $RPM_BUILD_ROOT/%{_prefix}/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/xgnokii
%{_datadir}/xgnokii/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*

%changelog
* Mon Jan  21 2008 - moinak.ghosh@sun.com
- Initial spec.
