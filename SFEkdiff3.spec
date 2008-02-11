#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEkdiff3
Summary:             Qt based diff -- compares or merges 2 or 3 files or directories
Version:             0.9.91
Source:              %{sf_download}/kdiff3/kdiff3-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEqt
BuildRequires: SFEqt-devel

%prep
%setup -q -n kdiff3-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

cd src-QT4

perl -i.orig -lpe 's/local\/// if $. == 51 || $. == 56' kdiff3.pro

qmake kdiff3.pro -o Makefile.qt
make -f Makefile.qt

%install
rm -rf $RPM_BUILD_ROOT

cd src-QT4
make -f Makefile.qt install INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kdiff3
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Fri Dec 07 2006 - Eric Boutilier
- Initial spec
