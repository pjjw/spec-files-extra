#
# spec file for package SFEsshmenu.spec
#
# includes module(s): sshmenu
#
%include Solaris.inc

%define src_name	sshmenu
%define src_url		http://www.mclean.net.nz/ruby/sshmenu/download

Name:                   SFEsshmenu
Summary:                SSH menu panel applet
Version:                3.13
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEruby-gnome2
Requires: SFEruby

%prep
%setup -q -n %{src_name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor || :
  touch %{_datadir}/icons/gnome || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/gnome || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  touch %{_datadir}/icons/gnome || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/gnome || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}
%defattr (-, root, other)
%{_datadir}/icons

%changelog
* Sun May 13 2007 - dougs@truemail.co.th
- Initial version
