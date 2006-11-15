# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# This is a set of GNU versions of commands that are in /usr/bin,
# So must relegate to /usr/gnu to avoid name collisions:

%define _prefix %{_basedir}/gnu

Name:			SFEdiffutils
Version:		2.8.1
Summary:		GNU diff
Source:			ftp://ftp.gnu.org/pub/gnu/diffutils/diffutils-%{version}.tar.gz
#Source2:                gendiff
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n diffutils-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
CFLAGS="$RPM_OPT_FLAGS"			\
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install \
    prefix=$RPM_BUILD_ROOT%{_prefix} \
    mandir=$RPM_BUILD_ROOT%{_mandir} \
    infodir=$RPM_BUILD_ROOT%{_infodir}
#/usr/ucb/install -m 0755 %SOURCE2 $RPM_BUILD_ROOT%{_bindir}/gendiff
rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/*

%changelog
* Wed Nov 15 2006  <eric.boutilier@sun.com>
- Copied and transposed CBEdiffutils to SFEdiffutils
* Tue Aug 22 2006  <laca@sun.com>
- fix %files attributes
- move to /opt/jdsbld by default
* Wed Aug 16 2006  <laca@sun.com>
- add missing deps
* Fri Dec 09 2005  <laca@sun.com>
- Add gendiff (taken from rpm 3.0.6, license: GPL)
* Fri Sep 02 2005  <laca@sun.com>
- remove unpackaged files
* Sun Sep 05 2004  <laca@sun.com>
- enable parallel build
* Tue Mar 09 2004  <laca@sun.com>
- initial version
