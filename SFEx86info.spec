#
# spec file for package SFEx86info
#
%include Solaris.inc
Name:                    SFEx86info
Summary:                 x86info - tool for reading cpu cpabilities
URL:                     http://www.codemonkey.org.uk/projects/x86info
Version:                 %(date +%Y.%m.%d)
Source:                  http://www.codemonkey.org.uk/projects/x86info/x86info-%git-snapshot.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc



%prep
%setup -q -c -n %name-%version

%build
cd x86info-*

#nothing to configure, just "make"
make

%install
rm -rf $RPM_BUILD_ROOT

cd x86info-*
mkdir -p $RPM_BUILD_ROOT/usr/sbin
cp -p x86info $RPM_BUILD_ROOT/usr/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*


%changelog
* Wed Oct 17 2007 - laca@sun.com
- fix issues with snapshot date
* Sat Aug 04 2007 - Thomas Wagner
- Initial spec
