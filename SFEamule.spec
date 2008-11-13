#
# spec file for package SFEamule
#
# includes module(s): amule
#
%include Solaris.inc

Name:                    SFEamule
Summary:                 aMule, an eMule-like client for the eD2k and Kademlia networks.
Version:                 2.2.2
Source:                  http://prdownload.berlios.de/amule/aMule-%{version}.tar.bz2
URL:                     http://www.amule.org/
SUNW_Copyright:          %{name}.copyright

# owner:alfred date:2008-07-16 type:bug
Patch1:                  amule-01-sun-studio12.patch

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWwxwidgets
Requires: SFEcryptopp-i386
BuildRequires: SUNWwxwidgets-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n aMule-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#export PATH="/usr/bin:$PATH"
export LDFLAGS="-norunpath"

autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir} --mandir=%{_mandir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/de
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/es
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/eu
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/fr
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/hu
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc(bzip2) -d docs COPYING license.txt Changelog AUTHORS README
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/xchat
%{_libdir}/xchat/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/amule
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/amule
%{_datadir}/doc/amule/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Nov 13 2008 - alfred.peng@sun.com
- Depends on SUNWwxwidgets and SUNWwxwidgets-devel instead.
* Sat Sep 27 2008 - alfred.peng@sun.com
- Initial version
