#
# spec file for package SFEdialog
#
# includes module(s): dialog
#

%include Solaris.inc

Name:                    SFEdialog
Summary:                 dialog - display dialog boxes from shell scripts
Group:                   utilities/scripting
%define year 2006
%define month  02
%define day    21
Version:		 1.0.%{year}.%{month}.%{day}
%define tarball_version  1.0-%{year}%{month}%{day}
Source:                  ftp://invisible-island.net/dialog/dialog-%{tarball_version}.tgz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{tarball_version}-build
%include default-depend.inc
Requires: SUNWlibms

%prep
%setup -q -n dialog-%tarball_version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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

%changelog
* Thu Jan 11 2007 - laca@sun.com
- fix version string to be numeric; use the versioned tarball
* Thu Jun 22 2006 - laca@sun.com
- rename to SFEdialog
- delete -share pkg
- remove unnecessary CFLAGS and LDFLAGS
- add missing dep
* Thu May 04 2006 - damien.carbery@sun.com
- Bump version to match dir name inside tarball. Fix share package perms.
* Sun Jan 29 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
