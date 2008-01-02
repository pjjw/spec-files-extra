#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEgpgme
Summary:             A C wrapper library for GnuPG
Version:             1.1.5
Source:              ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibgpg-error
Requires: SUNWlibgpg-error
Requires: SUNWtexi

%prep
%setup -q -n gpgme-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/libgpgme-pthread.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libgpgme-pth.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.la
rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%{_datadir}/common-lisp

%changelog
* Wed Jan 02 2008 - jijun.yu@sun.com
- Remove the unused file. 
* Mon Dec 17 2007 - jijun.yu@sun.com
- Bump to 1.1.5 and add some files to the package.
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Add '-lsocket -lnsl' to LDFLAGS for the accept/recvmsg/connect functions.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
