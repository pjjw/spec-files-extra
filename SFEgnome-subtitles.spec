#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEgnome-subtitles
Summary:             Video subtitling for the Gnome Desktop
Version:             0.4
Source:              http://downloads.sourceforge.net/gnome-subtitles/gnome-subtitles-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEmono-devel
BuildRequires: SFEgtk-sharp
BuildRequires: SFEgnome-sharp
Requires: SFEmono
Requires: SFEgtk-sharp
Requires: SFEgnome-sharp

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n gnome-subtitles-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%{optflags}"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_basedir}	\
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
	    --datadir=%{_datadir}	\
	    --mandir=%{_mandir}		\
	    --sysconfdir=%{_sysconfdir}	\
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
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%{_mandir}
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications
%{_datadir}/pixmaps

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sun Apr 22 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Add Build/Requires SFEmono-devel, SFEgtk-sharp, SFEgnome-sharp in order to
  get it to build.

* Sat Apr 21 2007 - dougs@truemail.co.th
- Initial spec
