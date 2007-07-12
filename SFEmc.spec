#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEmc
Summary:             Clone of the Norton Commander file manager
Version:             2007-06-23-14
Source:              http://www.ibiblio.org/pub/Linux/utils/file/managers/mc/snapshots/mc-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n mc-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

# I punted on building w/ nls and charset enabled. IOW, this
# spec file is in need of someone to give it some proper TLC.

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --libexecdir=%{_libexecdir} \
            --disable-nls  \
            --disable-charset

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rmdir ${RPM_BUILD_ROOT}%{_libexecdir}/mc
rmdir ${RPM_BUILD_ROOT}%{_libexecdir}
rmdir ${RPM_BUILD_ROOT}%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Thu Jul 12, 2007 - Dick Hoogendijk
- Changed to the snapshot release
- Stable version 4.6.1 has some nasty bugs
* Mon Sep 25, 2006 - Eric Boutilier
- Initial spec
