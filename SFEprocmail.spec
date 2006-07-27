#
# spec file for package SFEprocmail
#
# includes module(s): procmail
#
%include Solaris.inc

Name:                    SFEprocmail
Summary:                 Procmail
Version:                 3.22
Source:                  http://www.procmail.org/procmail-%{version}.tar.gz
Patch1:			 procmail-01-configuration.diff
Patch2:			 procmail-02-debian.diff
Patch3:			 procmail-03-large-files.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms


%prep
%setup -q -n procmail-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make BASENAME=${RPM_BUILD_ROOT}%{_prefix}	\
     MANDIR=${RPM_BUILD_ROOT}%{_mandir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/formail
%attr (2755,root,mail) %{_bindir}/lockfile
%{_bindir}/mailstat
%attr (6755,root,mail) %{_bindir}/procmail
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%changelog
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEprocmail
- remove unnecessary env variables
- update file attributes to match JDS
* Thu Oct 21 2005 - glynn.foster@sun.com
- Initial spec
