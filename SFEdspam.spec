#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEdspam
Summary:             Extremely scalable, statistical-hybrid anti-spam filter
Version:             3.6.8
Source:              http://www.nuclearelephant.com/projects/dspam/sources/dspam-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n dspam-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir} \
            --with-dspam-home=/var/dspam

# Notes: 
# I tried setting localstatedir instead of hard-coding
# /var/dspam (above), but it got ignored.
#
# If built with shared enabled and static disabled, the
# RPATH gets polluted with src/.libs. So for now I just
# went with the default: both enabled. Then I remove 
# libdspam.a (after install but before packaging, as usual).

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libdspam.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libdspam.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) /var/dspam
/var/dspam/*

%changelog
* Wed Oct 11 2006 - laca@sun.com
- fix pkgconfig dir permissions
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
