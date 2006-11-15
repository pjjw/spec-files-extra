# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# This is a set of GNU versions of commands that are in /usr/bin,
# so must relegate to /usr/gnu to avoid name collisions:

%define _prefix %{_basedir}/gnu

Name:			SFEfileutils
Summary:		GNU fileutils
Version:		4.1
Source:			ftp://ftp.gnu.org/pub/gnu/fileutils/fileutils-%{version}.tar.gz
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n fileutils-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export LINGUAS="xx"
%define _mandir %{_datadir}/man
CFLAGS="$RPM_OPT_FLAGS -xc99"			\
./configure --prefix=%{_prefix} --mandir=%{_mandir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT%{_prefix}/info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Wed Nov 15 2006  <eric.boutilier@sun.com>
- Copied and transposed CBEfileutils to SFEfileutils
* Tue Aug 22 2006  <laca@sun.com>
- fix %files attributes
- move to /opt/jdsbld by default
* Wed Aug 16 2006  <laca@sun.com>
- add missing deps
* Tue Aug  1 2006 - laca@sun.com
- add -xc99 (fix from Doug Scott)
* Fri Sep 02 2004  <laca@sun.com>
- remove unpackaged files
* Sun Sep 05 2004  <laca@sun.com>
- enable parallel build
* Fri Mar 05 2004  <laca@sun.com>
- fix %files
- change the pkg category
