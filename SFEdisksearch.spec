#
# spec file for package SFEdisksearch
#
# includes module(s): disksearch
#

%define PV 1.2.1
%define PN disksearch
%define PD A tool for searching for files on removable media disks
%define SRC_URI http://easynews.dl.sourceforge.net/%{PN}/
%define HOME http://%{PN}.sourceforce.org/
%define PROVIDES %{PN}-%{PV}

%include Solaris.inc
Name:                    SFE%{PN}
Summary:                 %{PN} - %{PD}
Version:                 %{PV}
Source:                  %{SRC_URI}/%{PN}-%{PV}.tar.gz
URL:			 %{HOME}		 
Patch1:					 disksearch-01-Makefile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:				SUNWPython
Requires:				SUNWGtku
Requires: SUNWgnome-python-libs
BuildRequires: SUNWgnome-python-libs-devel

%prep
%setup -q -n %{PN}-%{PV}
%patch1 -p1

%build
sed -i "s:/usr/local/share/disksearch:/usr/share/disksearch:" disksearch

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
make install prefix=/usr DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z][a-z]
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/disksearch
%{_datadir}/disksearch/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/[a-z]*
%endif




%changelog
* Mon Sep 10 2007 - flistellox@gmail.com
- Initial Specs
