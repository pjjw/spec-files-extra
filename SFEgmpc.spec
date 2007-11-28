#
# spec file for package SFEgmpc
#
# use gcc to compile

%include Solaris.inc
Name:                    SFEgmpc
Summary:                 gmpc - A gnome frontend for the mpd daemon
URL:                     http://sarine.nl/gmpc/
Version:                 0.15.1
Source:                  http://download.sarine.nl/gmpc-%{version}/gmpc-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:		 SFElibmpd-devel
BuildRequires:		 SFEcurl-devel
#test#BuildRequires:           SFEavahi-devel
Requires:		 SFElibmpd
Requires:		 SFEcurl
#test#Requires:		       SFEavahi
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gmpc-%version

%build
export LDFLAGS="-lX11"

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif

#TODO: check --disable-sm 
CC=$CC CXX=$CXX CFLAGS="$CFLAGS" ./configure --prefix=%{_prefix} \
            --disable-sm
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %{build_l10n}
%else
#rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gmpc
%{_datadir}/gmpc/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*



%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Wed Nov 28 2007 - Thomas Wagner
- remove (Build-)Requires: SFEavahi(-devel) - needs more love (change to SUNW... bonjour/avahi/zeroconf)
- change removal of "/locale" if !build_l10n to be rm -rf (diry not longer empty)
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
- pause avahi/zeroconf on client side (will be re-enabled later)
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
