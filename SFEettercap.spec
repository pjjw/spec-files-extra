#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# In a default configuration, non-root users can't run ettercap because
# they don't have priveleges to access the raw network interface (at least 
# that was my experience when I tested this).

%include Solaris.inc

Name:                SFEettercap
Summary:             MITM LAN attack prevention suite; includes graphical (gtk) support
Version:             0.7.3
Source:              http://%{sf_mirror}/sourceforge/ettercap/ettercap-NG-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWGtku
BuildRequires: SUNWxwxft
BuildRequires: SFElibpcap-devel
# Note: Apparently libnet is incapable of producing a shared lib...
BuildRequires: SFElibnet-devel
#
Requires: SUNWGtku
Requires: SUNWxwxft
Requires: SFElibpcap
Requires: %name-root

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

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir}	\
            --mandir=%{_mandir}		\
	    --enable-gtk		\
            --sysconfdir=%{_sysconfdir}

# I'm pretty sure that if ncurses and/or pcre are installed,
# those features will be automatically enabled at build-time.
# (not tested though.)

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/ettercap/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added %{_libdir} to %files
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Rename from ettercap-NG to ettercap; fix and adjust dependencies; force gcc
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
