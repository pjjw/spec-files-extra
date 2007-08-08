#
# spec file for package SFEwxwidgets
#
# includes module(s): wxWidgets
#

%include Solaris.inc

Name:                    SFEwxwidgets
Summary:                 wxWidgets - Cross-Platform GUI Library
URL:                     http://wxwidgets.org/
Version:                 2.8.4
%define tarball_version  2.8.4
Source:			 http://easynews.dl.sourceforge.net/sourceforge/wxwindows/wxWidgets-%{tarball_version}.tar.bz2
Patch1:                  wxwidgets-01-msgfmt.diff
Patch2:                  wxwidgets-02-sqrt.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs
Conflicts:     SFEwxGTK

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
%setup -q -n wxWidgets-%tarball_version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LD=/usr/ccs/bin/ld
export LDFLAGS="-lCrun -lCstd"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags -xlibmil -xlibmopt -features=tmplife"
./configure --prefix=%{_prefix}				\
			--bindir=%{_bindir}				\
			--includedir=%{_includedir}		\
			--libdir=%{_libdir}				\
			--with-gtk						\
			--enable-gtk2					\
			--enable-unicode				\
			--enable-mimetype				\
			--enable-gui					\
			--enable-xrc					\
			--with-expat					\
			--with-sdl						\
			--with-gnomeprint

make -j$CPUS
cd contrib
make -j$CPUS
cd ..
cd locale
make allmo
cd ..

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd contrib
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

cd $RPM_BUILD_ROOT%{_bindir}
rm -f wx-config
ln -s ../lib/wx/config/gtk2-unicode-release-* wx-config

%if %build_l10n
# Rename zh dir to zh_CN as zh is a symlink to zh_CN and causing installation
# problems as a dir.
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv zh zh_CN
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/bakefile
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bakefile/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Aug 07 2007 - nonsea@users.sourceforge.net
- Bump to 2.8.4
- Add --enable-gui --enable-xrc --with-expat for ./configure.
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Rename zh dir to zh_CN in %install as zh a symlink to zh_CN and causing
  installation problems as a dir.
* Tue Nov 28 2006 - laca@sun.com
- enable mimetype (wxUSE_MIMETYPE), needed by dvdstyler
- disable expat support as it conflicts with wxXML, which is also included
  in wxSVG
* Sat Oct 14 2006 - laca@sun.com
- fix wx-config to be a relative symlink
* Mon Jul 10 2006 - laca@sun.com
- rename to SFEwxwidgets
- delete -share subpkg
- delete unnecessary env variables
- fix building .mo files, add l10n subpkg
* Thu May 04 2006 - damien.carbery@sun.com
- Remove l10n package (no files in it, only empty dirs). Correct aclocal perms.
* Mon Mar 27 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
