#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Notes: This spec file will only work if CC is gcc. Do it at the command line
# before invoking this spec file (as opposed to putting it in %build below).
# That way the macros in Solaris.inc will know you've set it.
# 
# In a default configuration, non-root users can't run ettercap because
# they don't have priveleges to access the raw network interface (at least 
# that was my experience when I tested this).

%include Solaris.inc

Name:                SFEettercap-NG
Summary:             MITM LAN attack prevention suite; includes graphical (gtk) support
Version:             0.7.3
Source:              http://umn.dl.sourceforge.net/sourceforge/ettercap/ettercap-NG-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWGtku
BuildRequires: SUNWxwxft
BuildRequires: SFElibpcap
BuildRequires: SFElibnet
Requires: SUNWGtku
Requires: SUNWxwxft
Requires: SFElibpcap
Requires: SFElibnet

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n ettercap-NG-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --enable-gtk \
            --sysconfdir=%{_sysconfdir}

# I'm pretty sure that if ncurses and/or pcre are installed,
# those features will be automatically enabled at build-time.
# (not tested though.)

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* 
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
