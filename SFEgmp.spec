#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

Name:                    SFEgmp
Summary:                 GNU Multiple Presicion Arithmetic Library
Group:                   libraries/math
Version:                 4.2.1
Source:                  http://ftp.gnu.org/gnu/gmp/gmp-%{version}.tar.bz2
%ifarch amd64
Source1:                 http://www.loria.fr/~gaudry/mpn_AMD64/mpn_amd64.42.tgz
%endif
URL:                     http://swox.com/gmp/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEreadline-devel
Requires: SFEreadline

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr gmp-%{version} gmp-%{version}-64
%endif
%ifarch amd64
gtar fxz %{SOURCE1}
cd mpn_amd64.42
./install ../gmp-%{version}-64
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
export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags"

%ifarch sparcv9
export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"
%endif

%ifarch amd64
export CC="gcc"
export CXX=${CXX64:-$CXX}
export CFLAGS="-mtune=opteron -m64 -O3 -fomit-frame-pointer -fPIC -DPIC"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"
%endif


%ifarch amd64 sparcv9
cd gmp-%{version}-64

export ABI=64
./configure --prefix=%{_prefix}				\
	    --mandir=%{_mandir}				\
            --libdir=%{_libdir}/%{_arch64}		\
            --infodir=%{_infodir}			\
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      		\
            --disable-cxx
make -j$CPUS 
cd ..
%endif

cd gmp-%{version}

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"

export ABI=32
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --infodir=%{_infodir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-cxx
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gmp-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd gmp-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jun 30 2007 - nonsea@users.sourceforge.net
- Use http url in Source.
* Tue mar  7 2007 - dougs@truemail.co.th
- enabled 64-bit build and added speedup patch for AMD64
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgmp
- bump to 4.2.1
- create devel subpkg
- update attributes
* Thu Nov 17 2005 - laca@sun.com
- create
