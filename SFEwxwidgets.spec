#
# spec file for package SFEwxwidgets
#
# includes module(s): wxWidgets
#

%include Solaris.inc

Name:                    SFEwxwidgets
Summary:                 wxWidgets - Cross-Platform GUI Library
URL:                     http://wxwidgets.org/
Version:                 2.6.3
Source:			 http://easynews.dl.sourceforge.net/sourceforge/wxwindows/wxWidgets-%{version}.tar.bz2
Patch1:                  wxwidgets-01-msgfmt.diff
Patch11:                 wxgtk-01-sqrt.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs
Conflicts:     SFEwxGTK

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
%setup -q -n wxWidgets-%version
%patch1 -p1
%patch11 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags -xlibmil -xlibmopt -features=tmplife"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}			\
	    --with-gtk				\
	    --enable-gtk2			\
            --enable-unicode			\
            --with-sdl                          \
            --with-gnomeprint                   \
	    --enable-mimetype=no

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

%if %build_l10n
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
* Mon Jul 10 2006 - laca@sun.com
- rename to SFEwxwidgets
- delete -share subpkg
- delete unnecessary env variables
- fix building .mo files, add l10n subpkg
* Thu May 04 2006 - damien.carbery@sun.com
- Remove l10n package (no files in it, only empty dirs). Correct aclocal perms.
* Mon Mar 27 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
