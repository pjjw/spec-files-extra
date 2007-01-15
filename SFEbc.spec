#
# spec file for package SFEbc
#
# includes module(s): GNU bc
#
%include Solaris.inc

Name:                    SFEbc
Summary:                 GNU bc - arbitrary precision numeric processing language
Version:                 1.06
Source:			 http://ftp.gnu.org/gnu/bc/bc-%{version}.tar.gz
Patch1:                  bc-01-build.diff
URL:                     http://www.gnu.org/software/bc/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWpostrun
Requires: SFEreadline
Requires: SUNWtexi
BuildRequires: SFEreadline-devel

%prep
%setup -q -n bc-%version
%patch1 -p1 -b .patch01

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal
automake -a
autoconf
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
            --with-readline
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1gnu
mkdir -p $RPM_BUILD_ROOT%{_prefix}/gnu/bin

for f in bc dc; do
    mv $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/g$f
    cd $RPM_BUILD_ROOT%{_prefix}/gnu/bin
    ln -s ../bin/g$f $f
    cd $RPM_BUILD_ROOT%{_mandir}/man1
    sed -e 's/^\.TH \([^ ]*\) "*1"*/.TH \1 "1GNU"/' $f.1 > ../man1gnu/$f.1gnu
    rm -f $f.1
    ln -s ../man1gnu/$f.1gnu g$f.1
done

rm $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'bc.info dc.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'bc.info dc.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}/gnu
%dir %attr (0755, root, bin) %{_prefix}/gnu/bin
%{_prefix}/gnu/bin/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency.
* Sun Nov  5 2006 - laca@sun.com
- Create
