#
# spec file for package SFEx86info
#

# note: adjust to the version inside the x86info-%{version}.tar.gz
%define snapshotdate 2007-08-04

%include Solaris.inc
Name:                    SFEx86info
Summary:                 x86info - tool for reading cpu cpabilities
URL:                     http://www.codemonkey.org.uk/projects/x86info
Version:                 git-snapshot
Source:                  http://www.codemonkey.org.uk/projects/x86info/x86info-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc



%prep
%setup -q -n x86info-%{snapshotdate}

%build

#nothing to configure, just "make"

make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/sbin
cp -p x86info $RPM_BUILD_ROOT/usr/sbin


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*


%changelog
* Sat Aug 04 2007  - Thomas Wagner
- Initial spec
