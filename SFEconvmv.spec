#
# spec file for package SFEconvmv
#

%include Solaris.inc
Name:                    SFEconvmv
Summary:                 convmv - tool to convert filenames between locale
URL:                     http://http://www.j3e.de/linux/convmv/
#URL2:		http://www.linuxwiki.de/convmv
Version:                 1.12
Source:                  http://www.j3e.de/linux/convmv/convmv-%{version}.tar.gz
Patch1:			convmv-01-PREFIX.diff



SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO# Perl 5.8 is needed
#TODO: Reqirements:

%include default-depend.inc

%description
convmv is a small conversion utility for filenames (not file contents!) to convert special characters between different codepages.

convert all filenames in current workingdirectory and below from ISO-8859-15 to UTF-8:

convmv -f iso-8859-15 -t utf-8 -r .

same, from cp850 (old DOSsish) to utf-8:
convmv -f cp850 -t utf-8 -r .

Change all filenames in current workingdirectory and below to/from upper/lower case:

convmv --upper -r .
(resp. --lower for lowercase conversion)


%prep
%setup -q -n convmv-%version
%patch1 -p1

%build

#make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sun Oct 05 2008  - Thomas Wagner
- Initial spec. #TODO# add Requirements (Perl 5.8?)
