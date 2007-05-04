# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

# This is a set of GNU versions of commands that are in /usr/bin,
# So must relegate to /usr/gnu to avoid name collisions:

%define _prefix %{_basedir}/gnu

Name:			SFEcpio
Version:		2.7
Summary:		GNU cpio
Source:			ftp://ftp.gnu.org/pub/gnu/cpio/cpio-%{version}.tar.bz2
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n cpio-%{version}

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
rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}/libexec
%{_prefix}/libexec/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1


%changelog
* Mon Apr 16 2007  Thomas Wagner
- initial version (need relative restore from gnu cpio)