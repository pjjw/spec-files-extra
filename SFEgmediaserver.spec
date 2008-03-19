#
# spec file for package SFEgmediaserver
#
# includes module(s): gmediaserver
#
%include Solaris.inc

%define	src_name gmediaserver
%define	src_url	http://download.savannah.gnu.org/releases/%{src_name}

Name:                SFEgmediaserver
Summary:             GMediaServer is a UPnP compatible media server
Version:             0.12.0
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     gmediaserver-01-wall.diff
Patch2:		     gmediaserver-02-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWid3lib-devel
Requires: SUNWid3lib
BuildRequires: SFElibupnp-devel
Requires: SFElibupnp
Requires: SFEfile

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/gnu/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmediaserver.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmediaserver.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%{_mandir}

%changelog
* Sun Jul 15 2007 - dougs@truemail.co.th
- Initial spec
