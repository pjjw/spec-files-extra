#
# spec file for package SFEscalpel
#

%define src_name scalpel

%include Solaris.inc
Name:                    SFEscalpel
Summary:                 scalpel - A Frugal, High Performance File Carver
URL:                     http://www.digitalforensicssolutions.com/Scalpel/
Version:                 1.60
Source:                  http://www.digitalforensicssolutions.com/Scalpel/%{src_name}-%{version}.tar.gz
Patch1:                  scalpel-01-add-SOLARIS-add-timersub.diff


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc



%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build

make solaris

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -p %{src_name} $RPM_BUILD_ROOT/usr/bin/
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
cp -p %{src_name}.1 $RPM_BUILD_ROOT/usr/share/man/man1/
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{src_name}
cp -p %{src_name}.conf $RPM_BUILD_ROOT/usr/share/doc/%{src_name}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*



%changelog
* Sun May 18 2008  - Thomas Wagner
- Initial spec
