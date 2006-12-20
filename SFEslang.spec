#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEslang
Summary:             multi-platform programmer's library
Version:             2.0.5
Source:              ftp://space.mit.edu/pub/davis/slang/v2.0/slang-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWpng

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n slang-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L../src/elfobjs"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS elf

%install
rm -rf $RPM_BUILD_ROOT
make install-elf DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/libslang.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/slang
%dir %attr (0755, root, other) %{_libdir}/slang/v2
%dir %attr (0755, root, other) %{_libdir}/slang/v2/modules
%{_libdir}/slang/v2/modules/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/slsh
%{_datadir}/slsh/*.sl
%dir %attr (0755, root, other) %{_datadir}/slsh/local-packages
%dir %attr (0755, root, other) %{_datadir}/slsh/scripts
%{_datadir}/slsh/scripts/*
%dir %attr (0755, root, other) %{_datadir}/slsh/cmaps
%{_datadir}/slsh/cmaps/*
%dir %attr (0755, root, other) %{_datadir}/slsh/help
%{_datadir}/slsh/help/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/slang
%dir %attr (0755, root, other) %{_datadir}/doc/slang/v2
%{_datadir}/doc/slang/v2/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/slsh.rc

%changelog
* 
* Thu Dec 14 2006 - Eric Boutilier
- Initial spec
