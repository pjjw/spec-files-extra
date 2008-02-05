#
# spec file for package SFEcompiz
#

%include Solaris.inc

%define X11_DIR %{_prefix}/X11

Name:           SFEavant
Summary:        Avant Window Navigator - fully customizable dock-like navigator
Version:        0.2.1
Source:		http://launchpad.net/awn/0.2/0.2.1/+download/avant-window-navigator-%{version}.tar
Source1:        x11.pc
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires: 	SFEcompiz
Requires: 	SUNWdbus
Requires: 	SUNWgnome-base-libs
BuildRequires: 	SUNWdbus-devel
BuildRequires: 	SUNWgnome-base-libs-devel

%package devel
Summary:		 %summary - developer files
sUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
rm -rf avant-window-navigator-0.2.1
gunzip -c %{SOURCE} | tar xf -
cd avant-window-navigator-0.2.1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{X11_DIR}/lib/pkgconfig
cd avant-window-navigator-%{version}

if [ ! `pkg-config --exists x11` ]
then
	cp %{SOURCE1} ${RPM_BUILD_ROOT}
	export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${RPM_BUILD_ROOT}
fi

export CFLAGS="%optflags -I%{X11_DIR}/include" 
export LDFLAGS="-L$PROTO_LIB -L%{X11_DIR}/lib -R%{X11_DIR}/lib"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir}	\
	    --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
	    --datadir=%{_datadir}	

make -j$CPUS

%install

cd avant-window-navigator-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}/x11.pc

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

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
%dir %attr (0755, root, bin) %{_libdir}/awn
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%{_libdir}/*.so*
%{_libdir}/awn/*
%{_libdir}/python2.4/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/avant-window-navigator
%{_datadir}/avant-window-navigator/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Feb 05 2008 - Moinak Ghosh <moinak.ghosh@sun.com>
- Initial spec.
