#
# spec file for package SFEmrxvt
#
# includes module(s): Mrxvt
#
%include Solaris.inc

%define src_name	mrxvt
%define src_version	0.5.2
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	/

Name:                    SFEmrxvt
Summary:                 Mrxvt - A light weight terminal emulator
Version:                 %{src_version}
Source:                  http://umn.dl.sourceforge.net/sourceforge/materm/%{src_name}-%{version}.tar.gz
URL:                     http://materm.sourceforge.net/wiki/Main/HomePage
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch0:                  mrxvt-01-%{version}.sunstudio.diff

Requires: SUNWcsu

%prep
%setup -q -n %{src_name}-%version
%patch0 -p1

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --enable-24bits --enable-xft --with-term=xterm
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/mrxvt
%{_datadir}/doc/mrxvt/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%dir %attr(0755, root, sys) %{_sysconfdir}
%dir %attr(0755, root, sys) %{_sysconfdir}/mrxvt
%{_sysconfdir}/mrxvt/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial mrxvt spec file

