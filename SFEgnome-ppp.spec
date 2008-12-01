#
# spec file for package SFEgnome-ppp
#
# includes module(s): gnome-ppp
#
%include Solaris.inc

Name:                    SFEgnome-ppp
Summary:                 Modem internet connection tool for the GNOME Desktop
Version:                 0.3.23
Source:                  http://ftp.de.debian.org/debian/pool/main/g/gnome-ppp/gnome-ppp_%{version}.orig.tar.gz
URL:                     http://packages.debian.org/source/etch/gnome-ppp
Patch1:                  gnome-ppp-01-solaris-build.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel
Requires: SUNWlibC

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gnome-ppp-%{version}
#%setup -q
tar jxvf gnome-ppp-%{version}.tar.bz2
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd gnome-ppp-%{version}

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

cd gnome-ppp-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/gnome-ppp
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/*/apps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Dec 01 2008 - alfred.peng@sun.com
- Initial version
