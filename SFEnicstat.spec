#
# spec file for package SFEnicstat
#
%include Solaris.inc
Name:                    SFEnicstat
Summary:                 nicstat - tool for displaying network load similar to iostat/prstat
URL:                     http://blogs.sun.com/timc/entry/nicstat_the_solaris_network_monitoring
Version:                 %(date +%Y.%m.%d)
Source:                  http://blogs.sun.com/roller/resources/timc/nicstat.c


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc


%prep
rm -rf %name-%version
mkdir %name-%version
cd %name-%version
cp -p $RPM_SOURCE_DIR/nicstat.c .

%build
cd %name-%version

#nothing to configure, just "compile" it with this command: (see comments in source code)
cc -lgen -lkstat -lrt -lsocket -o nicstat nicstat.c


%install
rm -rf $RPM_BUILD_ROOT

cd %name-%version
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -p nicstat $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*


%changelog
* Wed Jan 02 2008 - Thomas Wagner
- Initial spec
