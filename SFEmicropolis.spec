#
# spec file for package SFEmicropolis
#

%include Solaris.inc
Name:                    SFEmicropolis
Summary:                 micropolis - Simulation game based on opensourced components of Simcity. 
URL:                     http://www.donhopkins.com/home/micropolis/ 
Version:                 1.0.0
Source:                  http://www.donhopkins.com/home/micropolis/micropolis-activity-source.tgz
Patch1:			 micropolis-01-solaris.diff
%define _optdir        /opt
SUNW_BaseDir:            %{_optdir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q  -n micropolis-activity

cp %SOURCE0 .
%patch1 -p1

%build
cd src
make

%install
rm -rf $RPM_BUILD_ROOT/%{_optdir}/sim
cd src
make install
cd ..
mkdir -p $RPM_BUILD_ROOT/%{_optdir}/sim
cp -r res $RPM_BUILD_ROOT/%{_optdir}/sim 
cp -r images $RPM_BUILD_ROOT/%{_optdir}/sim
cp -r cities $RPM_BUILD_ROOT/%{_optdir}/sim
cp -r manual $RPM_BUILD_ROOT/%{_optdir}/sim
cp -r activity $RPM_BUILD_ROOT/%{_optdir}/sim
cp Micropolis* $RPM_BUILD_ROOT/%{_optdir}/sim
cp README $RPM_BUILD_ROOT/%{_optdir}/sim


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_optdir}/sim/res/*
%{_optdir}/sim/images/*
%{_optdir}/sim/cities/*
%{_optdir}/sim/manual/*
%{_optdir}/sim/activity/*
%{_optdir}/sim/Micropolis*
%{_optdir}/sim/README


%changelog
* Wed Jan 23 2008 - Brian Nitz - <brian dot nitz at sun dot com> 
- Initial version.
