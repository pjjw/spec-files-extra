#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.8

Name:                SFEkdesdk3
Summary:             A collection of applications and tools used by KDE developers
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdesdk-%{version}.tar.bz2
Patch1:              kdesdk-01-kbabel.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SUNWsvn
Requires: SFElibapr
BuildRequires: SFElibapr-devel
Requires: SFEaprutil
BuildRequires: SFEaprutil-devel
Requires: SFEsubversion
BuildRequires: SFEsubversion-devel
Requires: SFEarts
BuildRequires: SFEarts-devel
Requires: SUNWperl584core
Requires: SUNWperl584usr
Requires: SUNWbison
Requires: SFEdoxygen
Requires: SUNWflexlex

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEkdebase3-devel
Requires: SFElibapr-devel
Requires: SFEaprutil-devel
Requires: SFEsubversion-devel
Requires: SFEarts-devel

%prep
%setup -q -n kdesdk-%version
#%patch1 -p1

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH="${PATH}:/usr/perl5/5.8.4/bin"
export CFLAGS="%optflags -fPIC -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/sfw/include" \
           --with-ssl-dir=/usr/sfw \
           --with-subversion \
           --with-subversion-dir=/usr/gnu \
           --with-apr-config=/usr/gnu/bin/apr-1-config \
           --with-apu-config=/usr/gnu/bin/apu-1-config


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.la*
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/mimelnk
%{_datadir}/mimelnk/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/servicetypes
%{_datadir}/servicetypes/*

%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
