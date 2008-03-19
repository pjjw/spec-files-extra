#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.8
%define ruby_bin /usr/ruby/1.8/bin

Name:                SFEamarok1
Summary:             A KDE based music player for Linux and Unix
Version:             1.4.8
Source:              http://download.kde.org/stable/amarok/%{version}/src/amarok-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# This also brings in all relevenat deps including kdelibs, qt, aRts and others.
Requires: SFEkdebase3
BuildRequires: SFEkdebase3-devel
Requires: SUNWlibusb
BuildRequires: SUNWlibusb
Requires: SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SFExmms1
BuildRequires: SFExmms1-devel
Requires: SFEkdemultimedia3
BuildRequires: SFEkdemultimedia3-devel
Requires: SUNWpostgr
BuildRequires: SUNWpostgr-devel
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-common-devel
BuildRequires: SFEdoxygen
Requires: SFEgraphviz
BuildRequires: SFEgraphviz-devel
Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3
Requires: SFElibmusicbrainz3
BuildRequires: SFElibmusicbrainz3-devel
Requires: SFElibtunepimp
BuildRequires: SFElibtunepimp-devel
BuildRequires: SFElibnjb
Requires: SFExine-lib
BuildRequires: SFExine-lib-devel
Requires: SUNWruby18u
BuildRequires: SUNWruby18u
Requires: SFElibvisual
BuildRequires: SFElibvisual-devel
Requires: SFElibvisual-plugins

%package encumbered
Summary:                 %{summary} - support for encumbered libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n amarok-%version

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{sfw_inc} -I%{gnu_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{sfw_inc} -I%{gnu_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%{xorg_lib_path} %{sfw_lib_path} %{gnu_lib_path} -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"

export QTDOCDIR=%{_datadir}/qt3/doc/html
export RUBY=%{ruby_bin}/ruby
extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"
sfw_prefix=`dirname %{sfw_bin}`

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --with-extra-includes="${extra_inc}" \
           --with-ssl-dir="${sfw_prefix}" \
           --enable-postgresql \
           --with-libnjb \
           --disable-debug


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

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
%{_libdir}/kde3/konqsidebar_universalamarok.so
%{_libdir}/kde3/konqsidebar_universalamarok.la
%{_libdir}/kde3/libamarok_void-engine_plugin.so
%{_libdir}/kde3/libamarok_void-engine_plugin.la
%{_libdir}/kde3/libamarok_xine-engine.so
%{_libdir}/kde3/libamarok_xine-engine.la
%{_libdir}/kde3/libamarok_generic-mediadevice.so
%{_libdir}/kde3/libamarok_generic-mediadevice.la
%{_libdir}/kde3/libamarok_daap-mediadevice.so
%{_libdir}/kde3/libamarok_daap-mediadevice.la
%{_libdir}/kde3/libamarok_massstorage-device.so
%{_libdir}/kde3/libamarok_massstorage-device.la
%{_libdir}/kde3/libamarok_nfs-device.so
%{_libdir}/kde3/libamarok_nfs-device.la
%{_libdir}/kde3/libamarok_smb-device.so
%{_libdir}/kde3/libamarok_smb-device.la
%dir %attr (0755, root, other) %{_libdir}/ruby_lib
%{_libdir}/ruby_lib/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/servicetypes
%{_datadir}/servicetypes/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*

%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files encumbered
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/libamarok_njb-mediadevice.so
%{_libdir}/kde3/libamarok_njb-mediadevice.la

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Jan 29 2008 - moinak.ghosh@sun.com
- Added dependency to libvisual and libvisual-plugins.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Initial spec.
