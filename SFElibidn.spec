#
# spec file for package SFElibidn
#
# includes module(s): GNU libidn
#
%include Solaris.inc

Name:                SFElibidn
Summary:             GNU IDN conversion library
Version:             1.5
Source:              http://alpha.gnu.org/pub/gnu/libidn/libidn-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libidn-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}         \
           --mandir=%{_mandir}         \
           --infodir=%{_infodir}       \
           --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# This source doesn't provide a --without-emacs option,
# thus we have ensure there won't be any site-lisp files:
rm -rf $RPM_BUILD_ROOT%{_datadir}/emacs

rm $RPM_BUILD_ROOT%{_infodir}/dir

rm $RPM_BUILD_ROOT%{_libdir}/libidn.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
 echo 'infos="';
 echo 'libidn.info' ;
 echo '"';
 echo 'retval=0';
 echo 'for info in $infos; do';
 echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
 echo 'done';
 echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
 echo 'infos="';
 echo 'libidn.info' ;
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
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/rw/LC_MESSAGES/libidn.mo
%{_datadir}/locale/cs/LC_MESSAGES/libidn.mo
%{_datadir}/locale/fr/LC_MESSAGES/libidn.mo
%{_datadir}/locale/nl/LC_MESSAGES/libidn.mo
%{_datadir}/locale/pl/LC_MESSAGES/libidn.mo
%{_datadir}/locale/zh_CN/LC_MESSAGES/libidn.mo
%{_datadir}/locale/en@boldquot/LC_MESSAGES/libidn.mo
%{_datadir}/locale/ro/LC_MESSAGES/libidn.mo
%{_datadir}/locale/it/LC_MESSAGES/libidn.mo
%{_datadir}/locale/eo/LC_MESSAGES/libidn.mo
%{_datadir}/locale/sr/LC_MESSAGES/libidn.mo
%{_datadir}/locale/da/LC_MESSAGES/libidn.mo
%{_datadir}/locale/vi/LC_MESSAGES/libidn.mo
%{_datadir}/locale/de/LC_MESSAGES/libidn.mo
%{_datadir}/locale/ja/LC_MESSAGES/libidn.mo
%{_datadir}/locale/fi/LC_MESSAGES/libidn.mo
%{_datadir}/locale/en@quot/LC_MESSAGES/libidn.mo
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Oct 14 2008 - michal.bielicki@halokwadrat.de
- Why does everyone dislike .mo files ?
* Thu Mar 06 2008 - nonsea@users.sourceforge.net
- Bump to 1.5
* Wed Aug 08 2007 - nonsea@users.sourceforge.net
- Bump to 1.0
* Sun Mar 04 2007 - Eric Boutilier
- Initial spec
