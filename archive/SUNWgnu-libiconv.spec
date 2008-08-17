#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define _prefix /usr/gnu

Name:                SUNWgnu-libiconv
Summary:             GNU iconv -- Code set conversion
Version:             1.12
Source:              http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
Patch1:              libiconv-01-fix-runpath.diff
Patch2:              libiconv-02-646.diff
Patch3:              libiconv-03-intmax.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:       SFEgperf

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd libiconv-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr libiconv-%{version} libiconv-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export CXXFLAGS32="%cxx_optflags"
export CXXFLAGS64="%cxx_optflags64"

%ifarch amd64 sparcv9

export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$CFLAGS64"

cd libiconv-%{version}-64

# regenerate aliases.h after adding 646 in patch2
# requires gperf
make -f Makefile.devel lib/aliases.h

libtoolize --force
aclocal -I m4
autoconf
./configure \
        --prefix=%{_prefix}	\
        --bindir=%{_bindir}/%{_arch64} \
        --libdir=%{_libdir}/%{_arch64}	\
        --datadir=%{_datadir}	\
        --mandir=%{_mandir}	\
        --disable-nls \
        --disable-static

make -j$CPUS
cd ..
%endif

cd libiconv-%{version}

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$CFLAGS32"

# regenerate aliases.h after adding 646 in patch2
# requires gperf
make -f Makefile.devel lib/aliases.h

libtoolize --force
aclocal -I m4
autoconf
./configure \
        --prefix=%{_prefix}	\
        --libdir=%{_libdir}	\
        --datadir=%{_datadir}	\
        --mandir=%{_mandir}	\
        --disable-nls \
        --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd libiconv-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.la
rm -r $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
cd ..
%endif

cd libiconv-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

mkdir -p $RPM_BUILD_ROOT%{_basedir}/lib
cd $RPM_BUILD_ROOT%{_basedir}/lib
ln -s ../gnu/lib/libiconv.so libgnuiconv.so
ln -s libgnuiconv.so libiconv.so

%ifarch amd64 sparcv9
mkdir -p %{_arch64}
cd %{_arch64}
ln -s ../../gnu/lib/%{_arch64}/libiconv.so libgnuiconv.so
ln -s libgnuiconv.so libiconv.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/iconv
%dir %attr (0755, root, bin) %{_basedir}/lib
%{_basedir}/lib/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/charset.alias
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%{_libdir}/%{_arch64}/charset.alias
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/iconv.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/iconv*.3

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Bump to 1.12
- Add patch intmax.diff to fix build issue.
* Sat Sep 29 2007 - laca@sun.com
- add /usr/lib/libiconv.so symlink so that less spec file changes
  and patches are needed for using GNU libiconv instead of the libc
  iconv implementation
* Fri Sep 28 2007 - laca@sun.com
- fix %install and %files
* Sun Apr 21 2007 - Doug Scott
- Added -L/usr/gnu/lib -R/usr/gnu/lib
* Mon Mar 12 2007 - Eric Boutilier
- Initial spec
