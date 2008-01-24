#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.8

%define broken_netsnmp %([ -f %{sfw_lib}/libnetsnmp.la ] && echo 1 || echo 0)
Name:                SFEkdeutils3
Summary:             A collection of useful utilities in official KDE
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdeutils-%{version}.tar.bz2
Patch1:              kdeutils-01-khexedit.diff
Patch2:              kdeutils-02-superkaramba.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SUNWPython
Requires: SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEarts
BuildRequires: SFEarts-devel
BuildRequires: SFEdoxygen
Requires: SFExmms1
BuildRequires: SFExmms1-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEkdebase3-devel
Requires: SFEgmp-devel
Requires: SFEarts-devel
Requires: SFExmms1-devel

%prep
%setup -q -n kdeutils-%version
%patch1 -p1
%patch2 -p1

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
export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

export LIBS=$LDFLAGS

export PATH="${PATH}:/usr/openwin/bin"
extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
%if %broken_netsnmp
           --with-extra-includes="${extra_inc}" \
           --with-snmp=no
%else
           --with-extra-includes="${extra_inc}"
%endif


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Get rid of irkick. IrDA is yet unsupported on Solaris
#
(cd ${RPM_BUILD_ROOT}
  find . \( -name "irkick*" -a -type d \) | xargs rm -rf
  find . \( -name "irkick*" -a -type f \) | xargs rm -f
)

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
%dir %attr (0755, root, other) %{_datadir}/applnk
%{_datadir}/applnk/*
%dir %attr (0755, root, other) %{_datadir}/mimelnk
%{_datadir}/mimelnk/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/servicetypes
%{_datadir}/servicetypes/*

%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Initial spec.
