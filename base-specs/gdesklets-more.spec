#
# spec file for package gdesklets-extra
#
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

%define gdesklets_quote_of_day 0.61
%define gdesklets_Sudoku 0.3
%define gdesklets_newsgrab 1.5
%define gdesklets_desklet 0.01

Name:           gdesklets-extra
Summary:        Unsuportted extra desklets package
Release:        1
License:	GPL
Group:		Applications/Internet
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Useful desklets
Source0:        http://www.gdesklets.de/files/desklets/NewsGrab/NewsGrab-%{gdesklets_newsgrab}.tar.gz 
Source1: 	http://gdesklets.zencomputer.ca/Quote_of_the_Day-%{gdesklets_quote_of_day}.tar.gz
Source2:	http://gdesklets.zencomputer.ca/Sudoku-%{gdesklets_Sudoku}.tar.gz
URL:		http://gdesklets.zencomputer.ca/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Autoreqprov:	on

%prep


%build
# we just get the bits tarball from developer

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdesklets/Controls
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdesklets/Displays
cd $RPM_BUILD_ROOT%{_datadir}/gdesklets/Controls
mkdir NewsGrab
cd $RPM_BUILD_ROOT%{_datadir}/gdesklets/Displays
/usr/sfw/bin/gtar -zxf %{SOURCE0}
mv NewsGrab/controls $RPM_BUILD_ROOT%{_datadir}/gdesklets/Controls/NewsGrab
/usr/sfw/bin/gtar -zxf %{SOURCE1}
/usr/sfw/bin/gtar -zxf %{SOURCE2}
mv Displays/Sudoku .
rm -r Displays
mv controls/Sudoku $RPM_BUILD_ROOT%{_datadir}/gdesklets/Controls
rm -r controls

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir %attr (0755, root, root) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/gdesklets
%{_datadir}/gdesklets/*

%changelog

* Thu Jan 25 2008 - <chris.wang@sun.com>
- initial creation


