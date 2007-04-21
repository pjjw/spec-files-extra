#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEmailnotify
Summary:             Mail Notification panel applet
Version:             4.0
Source:              http://savannah.nongnu.org/download/mailnotify/mail-notification-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibnotify-devel
Requires: SUNWlibnotify
BuildRequires: SUNWgnome-panel-devel
Requires: SUNWgnome-panel
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n mail-notification-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%{optflags} -I/usr/sfw/include"
export LDFLAGS="%_ldflags -lX11 -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_basedir}	\
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
	    --datadir=%{_datadir}	\
	    --mandir=%{_mandir}		\
	    --sysconfdir=%{_sysconfdir}	\
	    --enable-ssl		\
	    --disable-evolution		\
	    --disable-debug

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
  touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/omf
%{_datadir}/mail-notification
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%defattr (-, root, other)
%{_datadir}/applications
%{_datadir}/icons
%{_datadir}/locale

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added Requires: SUNWlibnotify
* Fri Apr 20 2007 - dougs@truemail.co.th
- Initial spec
