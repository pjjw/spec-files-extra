#
# spec file for package SFEasciidoc
#
# includes module(s): asciidoc
#

%include Solaris.inc

Name:                    SFEasciidoc
Summary:                 AsciiDoc - Text based document generation
Version:                 8.2.2
URL:                     http://www.methods.co.nz/asciidoc/
Source:			 http://www.methods.co.nz/asciidoc/asciidoc-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWPython
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
%setup -q -n asciidoc-%version

%build
perl -pi -e 's,^BINDIR=.*,BINDIR=%{buildroot}%{_bindir},' install.sh
perl -pi -e 's,^MANDIR=.*,MANDIR=%{buildroot}%{_mandir},' install.sh
perl -pi -e 's,^CONFDIR=.*,CONFDIR=%{buildroot}%{_sysconfdir}/asciidoc,' install.sh

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
bash ./install.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/asciidoc

%changelog
* Mon Aug 06 2007 - brian.cameron@sun.com
- Bump to 8.2.2.
* Fri Jun 22 2007 - laca@sun.com
- bump to 8.2.1
* Tue Feb 13 2007 - laca@sun.com
- create
