# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:			SFEautomake
Version:		1.9.6
Vendor:			Sun Microsystems, Inc.
Source:			ftp://ftp.gnu.org/pub/gnu/automake/automake-%{version}.tar.bz2
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:               SUNWperl584core
Requires:               SFEm4

%prep
%setup -q -n automake-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
CFLAGS="$RPM_OPT_FLAGS"			\
./configure \
    --prefix=%{_prefix}         \
    --infodir=%{_infodir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# make aclocal always look for macros in /usr/share/aclocal
test "%{_datadir}" = "/usr/share" || \
    echo "/usr/share/aclocal" > $RPM_BUILD_ROOT%{_datadir}/aclocal/dirlist

# Uncomment the following if %{_datadir} is not /usr/share
# mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal

rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/aclocal-*
%{_datadir}/automake-*

# Uncomment the following if %{_datadir} is not /usr/share
# %dir %attr (0755, root, other) %{_datadir}/aclocal
# %{_datadir}/aclocal/*

%changelog
* Wed Nov 15 2006  <eric.boutilier@sun.com>
- Copied and transposed CBEautomake to SFEautomake
* Tue Aug 22 2006  <laca@sun.com>
- fix %files attributes
- move to /opt/jdsbld by default
* Wed Aug 16 2006  <laca@sun.com>
- add missing deps
* Tue Oct 18 2005 - <laca@sun.com>
- add /usr/share/aclocal to the default search path
* Wed Aug 31 2005 - <laca@sun.com>
- update to 1.9.6
* Sun Sep 05 2004 - <laca@sun.com>
- enable parallel build
* Fri Mar 05 2004 - <laca@sun.com>
- fix %files
- change the pkg category
