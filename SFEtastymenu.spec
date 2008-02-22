#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define SFEfreetype %(/usr/bin/pkginfo -q SFEfreetype && echo 1 || echo 0)

Name:                SFEtastymenu
License:             GPL,LGPL
Summary:             A K-Menu replacement for KDE 3.x
Version:             1.0.7
URL:                 http://www.notmart.org/tastymenu
Source:              http://www.notmart.org/files/tastymenu-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevant deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SFEfam
BuildRequires: SFEfam-devel
%if %SFEfreetype
Requires: SFEfreetype
BuildRequires: SFEfreetype-devel
%else
Requires: SUNWfreetype2
BuildRequires: SUNWfreetype2
%endif
Requires: SUNWlexpt
Requires: SUNWlibms
Requires: SUNWpng
Requires: SUNWxorg-clientlibs
Requires: SUNWxwplt
Requires: SUNWxwrtl
Requires: SUNWxwxft
Requires: SUNWzlib

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n tastymenu-%version

if [ "x`basename $CC`" != xgcc ]
then
	echo "This spec file requires Gcc, set the CC and CXX env variables"
    exit 1
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"
export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"
export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"
%if %SFEfreetype
export FREETYPE_CONFIG=%{sfw_bin}/freetype-config
%else
export FREETYPE_CONFIG=%{gnu_bin}/freetype-config
%endif

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --libdir=%{_libdir} \
           --datadir=%{_datadir} \
           --docdir=%{_docdir} \
           --enable-shared=yes \
           --enable-static=no \
           --with-extra-includes="${extra_inc}" \
           --enable-final

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Feb 23 2008 - ananth@sun.com
- Initial spec
