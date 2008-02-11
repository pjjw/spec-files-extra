#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEkipi-plugins
License:             LGPL
Summary:             Plugins for KDE Image Plugin Interface Library
Version:             0.1.5-rc1
URL:                 http://extragear.kde.org/apps/kipi/
Source:              %{sf_download}/kipi/kipi-plugins-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SFElibkipi
BuildRequires: SFElibkipi-devel
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n kipi-plugins-%version

if [ "x`basename $CC`" != xgcc ]
then
        %error This spec file requires Gcc, set the CC and CXX env variables
fi


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl"

extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no  \
            --enable-final	\
            --with-extra-includes="${extra_inc}"

make -j$CPUS
make apidox

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.la
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*
%endif

%changelog
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Initial spec.
