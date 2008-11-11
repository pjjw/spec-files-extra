#
# spec file for package SFEhamster
#
# includes module(s): hamster
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#


%include Solaris.inc

Name:                    SFEhamster
Summary:		 Time tracking for masses	
Version:                 2.24.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/hamster-applet/2.24/hamster-applet-%{version}.tar.gz
URL:                     http://live.gnome.org/ProjectHamster
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:     SUNWsqlite3
BuildRequires:     SUNWpysqlite
Requires:          SUNWsqlite3
Requires:          SUNWpysqlite
Requires:          SUNWlibC

%prep
%setup -q -n hamster-applet-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix} \
	    --bindir=%{_bindir}	\
	    --libdir=%{_libdir}	\
	    --mandir=%{_mandir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, root) %{_prefix}/etc
%{_prefix}/etc/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Tue Nov 11 2008 - jijun.yu@sun.com
- Add BuildRequires.
* Wed Oct 22 2008 - jijun.yu@sun.com
- Bump to 2.24.1
* Tue Oct 07 2008 - jijun.yu@sun.com
- Initial spec
