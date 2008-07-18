%include Solaris.inc

Name: bonnie++
Summary: Disk benchmark
Version: 1.03c
Release: 1
License: GPL
Group: System
Provides: bonnie++
Source0: http://www.coker.com.au/bonnie++/bonnie++-1.03c.tgz
Patch0: bonnie++.patch
BuildRoot: %{_tmppath}/%{name}-root
Packager: Will Murnane <willm1@cs.umbc.edu>
%ifos solaris
SUNW_Pkg: SFEbonnie++
%endif
%include default-depend.inc

%description
Bonnie++ is a benchmark suite that is aimed at performing a number of simple tests of hard drive and file system performance.

%prep
%setup -q
%patch0 -p1

%build
export PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/ccs/bin:/usr/openwin/bin:/usr/sfw/bin:/usr/java/bin:/opt/sfw/bin
CPPFLAGS='-I/usr/site/include' LDFLAGS='-L/usr/site/lib' ./configure --prefix=%{_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --mandir=%{_mandir}
gmake

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}/bon_csv2html
%{_bindir}/bon_csv2txt
%{_sbindir}/bonnie++
%{_sbindir}/zcav
%{_mandir}/man1/bon_csv2html.1
%{_mandir}/man1/bon_csv2txt.1
%{_mandir}/man8/bonnie++.8
%{_mandir}/man8/zcav.8

%changelog
* Wed Jun 11 2008 Will Murnane <will.murnane@gmail.com>
- Initial Package version 1.03c
