#
# spec file for package SFEmemcached
#
# includes module(s): memcached
#
%include Solaris.inc

Name:                    SFEmemcached
Summary:                 memcached - remote control software package derived from the popular VNC software
Version:                 1.2.1
Source:                  http://www.danga.com/memcached/dist/memcached-%{version}.tar.gz
Patch1:                  memcached-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SUNWxwrtl
#Requires: SUNWzlib
#Requires: SUNWlibms
#BuildRequires: SUNWxwopt

%prep
%setup -q -n memcached-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PATH=/usr/openwin/bin:${PATH}
export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}
	    
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Fri Jan 12 2007 - daymobrew@users.sourceforge.net
- Initial spec

