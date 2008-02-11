#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEgnome-subtitles
Summary:             Video subtitling for the Gnome Desktop
Version:             0.6
Source:              %{sf_download}/gnome-subtitles/gnome-subtitles-%{version}.tar.gz
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

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


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

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -r $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
%endif

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
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/gnome-subtitles/C
%{_datadir}/omf/gnome-subtitles/gnome-subtitles-C.omf

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-subtitles/[a-z]*
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/omf/gnome-subtitles/gnome-subtitles-[a-z][a-z].omf
%endif


%changelog
* Mon Nov 12 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Bump to 0.6. Add l10n package.

* Sun Apr 22 2007 - Damien Carbery <daymobrew@users.sourceforge.net>
- Add Build/Requires SFEmono-devel, SFEgtk-sharp, SFEgnome-sharp in order to
  get it to build.

* Sat Apr 21 2007 - dougs@truemail.co.th
- Initial spec
