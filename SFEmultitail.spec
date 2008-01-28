#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEmultitail
License:             GPL
Summary:             MultiTail follows files in style, it is tail on steroids.
Version:             5.2.0
URL:                 http://www.vanheusden.com/multitail/
Source:              http://www.vanheusden.com/multitail/multitail-%{version}.tgz
Patch1:              multitail-01-makefiles.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEncurses
BuildRequires: SFEncurses-devel

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n multitail-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export EXTRA_CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__"
export EXTRA_LDFLAGS="%_ldflags %{gnu_lib_path}"

if [ "x`basename $CC`" = xgcc ]
then
	make -f makefile.solaris_gcc
else
	make -f makefile.solaris_sunwspro
fi

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

if [ "x`basename $CC`" = xgcc ]
then
	make -f makefile.solaris_gcc install DESTDIR=$RPM_BUILD_ROOT
else
	make -f makefile.solaris_sunwspro install DESTDIR=$RPM_BUILD_ROOT
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Mon Jan 28 2008 - moinak.ghosh@sun.com
- Initial spec.
