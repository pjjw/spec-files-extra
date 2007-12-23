#
# spec file for package SFEwmctrl
#
# includes module(s): wmctrl
#
%include Solaris.inc

Name:                    SFEwmctrl
Summary:                 Wmctrl A command line tool to interact with an EWMH/NetWM compatible X Window Manager.
Version:                 1.07
Source:                  http://www.sweb.cz/tripie/utils/wmctrl/dist/wmctrl-%{version}.tar.gz
URL:                     http://www.sweb.cz/tripie/utils/wmctrl/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n wmctrl-%{version}

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

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
%{_datadir}/*

%changelog
- Dec 23 2007 - pradhap (at) gmail.com
- Initial Wmctrl spec file
