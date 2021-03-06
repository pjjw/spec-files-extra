#
# spec file for package SFEgmpc
#
# use gcc to compile
# works: snv104 / pkgbuild 1.3.91
# works: snv104 / pkgbuild 1.2.0
# works: snv96  / pkgbuild 1.3.1


%define version_sub 0

%include Solaris.inc


%define SUNWcurl      %(/usr/bin/pkginfo -q SUNWcurl   && echo 1 || echo 0)
%define SUNWgtkmm     %(/usr/bin/pkginfo -q SUNWgtkmm  && echo 1 || echo 0)

Name:                    SFEgmpc
Summary:                 gmpc - A gnome frontend for the mpd daemon
URL:                     http://sarine.nl/gmpc/
Version:                 0.15.5
Source:                  http://download.sarine.nl/Programs/gmpc/%{version}/gmpc-%{version}.%{version_sub}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}.%{version_sub}-build
BuildRequires:		 SFElibmpd-devel
#test#BuildRequires:           SFEavahi-devel
Requires:		 SFElibmpd

%if %SUNWcurl
BuildRequires:		SUNWcurl
Requires:		SUNWcurl
%else
BuildRequires:		 SFEcurl-devel
Requires:		 SFEcurl
%endif

%if %SUNWgtkmm
BuildRequires:		SUNWgtkmm-devel
Requires:		SUNWgtkmm
%else
BuildRequires:		SFEgtkmm-devel
Requires:		SFEgtkmm
%endif

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
%setup -q -n gmpc-%version.%{version_sub}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export LDFLAGS="%_ldflags -lnsl -lsocket -lresolv"

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif

#TODO: check --disable-sm 
CC=$CC CXX=$CXX CFLAGS="$CFLAGS" ./configure --prefix=%{_prefix} \
%if %SUNWcurl
            --with-curl=/usr \
%else
            --with-curl=/usr/gnu \
%endif
            #--disable-sm
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%if %{build_l10n}
%else
#rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog COPYING NEWS AUTHORS TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
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
* Mon Dec 22 2008 - Thomas Wagner
- add nice and clean conditional (Build-)Requires: %if %SUNWgtkmm ... %else ... SFEgtkmm(-devel)
- create %{_docdir} in case old pkgbuild doesn't
* Sat Dec 20 2008 - Thomas Wagner
- adjust download URL
- add nice and clean conditional (Build-)Requires: %if %SUNWcurl ... %else ... SFEcurl(-devel)
- add LDFLAGS for network libs
- reduce files in %doc, add permissions to %{_docdir}
* Thu Jan 03 2008 - Thomas Wagner
- enabled building in parallel
* Sun Dec 02 2007 - Thomas Wagner
- bump to 0.15.5.0, add version_sub (currently at "0")
- remove --disable-sm (Session Manager)
- switch to new location of SFEcurl --with-curl=/usr/gnu
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
