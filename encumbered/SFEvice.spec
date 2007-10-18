#
# spec file for package SFEvice.spec
#
# includes module(s): vice
#
%include Solaris.inc

%define src_name	vice
%define src_url		http://www.zimmers.net/anonftp/pub/cbm/crossplatform/emulators/VICE

Name:                   SFEvice
Summary:                CBM Emulator
Version:                1.21
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Source1:		CC-wrapper
Patch1:			vice-01-crun.diff
Patch2:			vice-02-fonts.diff
Patch3:			vice-03-locale.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEreadline-devel
Requires: SFEreadline
BuildRequires: SFElame-devel
Requires: SFElame

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
install -c -m 0755 %SOURCE1 .

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export CXX="$PWD/CC-wrapper"
export LDFLAGS="%{_ldflags} -L/usr/X11/lib -R/usr/X11/lib"
export PATH=$PATH:/usr/openwin/bin

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
automake --add-missing
autoconf --force

(
  cd src/resid
  libtoolize --copy --force
  aclocal $ACLOCAL_FLAGS
  automake --add-missing
  autoconf --force
)

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
            --enable-shared			\
	    --disable-static		

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_datadir}/info/dir

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'vice.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'vice.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%defattr (-, root, other)
%{_datadir}/locale

%changelog
* Thu Apr 26 2006 - dougs@truemail.co.th
- Initial version
