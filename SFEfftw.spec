#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEfftw
Summary:             Collection of fast C routines to compute DFTs
Version:             2.1.5
Source:              ftp://ftp.fftw.org/pub/fftw/fftw-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n fftw-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

# Can't figure out how to tell configure to install the provided
# html or ps docs... it installs the info files though. Punt.

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_infodir} \
            --enable-shared=yes \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/librfftw.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libfftw.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* 
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
