#
# spec file for package SFEnetpbm
#
# includes module(s): SFEnetpbm
#
%include Solaris.inc
# use the --with-svn-code option to use svn co instead of the stable tarball
%define svn_url https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced

Name:                    SFEnetpbm
Summary:                 netpbm - network portable bitmap tools
%if %{?_with_svn_code:0}%{?!_with_svn_code:1}
# stable tarball build
Version:                 10.26.46
Source:                  %{sf_download}/netpbm/netpbm-%{version}.tgz
%else
# svn code
Version:                 10.35
%endif
Patch1:			 netpbm-01-strings.diff
Patch2:			 netpbm-Makefile.conf
# Patch3:			 netpbm-02-stdlib.diff
Patch4:			 netpbm-03-no-XDefs.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%if %{?_with_svn_code:0}%{?!_with_svn_code:1}
# stable tarball build
%setup -q -n netpbm-%version
%else
# svn checkout
rm -rf netpbm-%version
mkdir netpbm-%version
cd netpbm-%version
rm -rf netpbm
[ ! -f ../../SOURCES/netpbm-%version.tar.bz2 ] && {
    svn checkout %{svn_url} netpbm
    tar fcp - netpbm | bzip2 -c > ../../SOURCES/netpbm-%version.tar.bz2
}
[ ! -d netpbm ] && bunzip2 -c ../../SOURCES/netpbm-%version.tar.bz2 | tar fxp -
cd netpbm
%patch1 -p1
# %patch3 -p1
%patch4 -p1
%endif
cat Makefile.config.in %{PATCH2} > Makefile.config
touch Makefile.depend

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"

%if %{?_with_svn_code:1}%{?!_with_svn_code:0}
# svn code
cd netpbm-%version
cd netpbm
%endif
make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
%if %{?_with_svn_code:1}%{?!_with_svn_code:0}
cd netpbm-%version
cd netpbm
%endif
mkdir $RPM_BUILD_ROOT
make package PKGDIR=$RPM_BUILD_ROOT/package
cd $RPM_BUILD_ROOT/package/lib
ln -s libnetpbm.so.10 libnetpbm.so
cd ..
mkdir -p $RPM_BUILD_ROOT/usr/share
mv bin $RPM_BUILD_ROOT/usr
mv include $RPM_BUILD_ROOT/usr
mv lib $RPM_BUILD_ROOT/usr
mv man $RPM_BUILD_ROOT/usr/share
mv misc $RPM_BUILD_ROOT/usr/share/netpbm
cd $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/package

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Oct 17 2007 - laca@sun.com
- use stable tarball by default, use svn checkout with --with-svn-code
* Tue Sep 18 2007 - markwright@internode.on.net
- Add netpbm. to svn_url
- Comment netpbm-02-stdlib.diff, as stdlib.h now included in generator/ppmrough.c
- Add patch4 netpbm-03-no-XDefs.diff
* Sat Apr 21 2007 - dougs@truemail.co.th
- Disabled parallel make. Can be a problem on a multicpu system
* Wed Feb 28 2007 - markgraf@med.ovgu.de
- need to include stdlib.h in generator/ppmrough.c
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
