#
# spec file for package SFEgmpc
#
# use gcc to compile

%include Solaris.inc
Name:                    SFEgmpc
Summary:                 gmpc - A gnome frontend for the mpd daemon
URL:                     http://sarine.nl/gmpc/
Version:                 0.14.0
Source:                  http://download.sarine.nl/gmpc-0.14.0/gmpc-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires:		 SFElibmpd-devel
BuildRequires:		 SFEcurl-devel
Requires:		 SFElibmpd
Requires:		 SFEcurl

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

#TODO: check --disable-sm 
./configure --prefix=%{_prefix} \
            --disable-sm
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
#TODO check if needed  # Rename pl_PL dir to pl as pl_PL is a symlink to pl and causing installation
#TODO check if needed  # problems as a dir.
#TODO check if needed  cd $RPM_BUILD_ROOT%{_datadir}/locale
#TODO check if needed  mv pl_PL pl
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
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
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
