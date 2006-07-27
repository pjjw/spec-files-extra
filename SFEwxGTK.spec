#
# spec file for package SFEwxGTK
#
# includes module(s): wxGTK
#
%include Solaris.inc

Name:                    SFEwxGTK
Summary:                 wxGTK a sophisticated cross-platform C++ framework for writing advanced GUI applications
Version:                 2.6.3
Source:                  http://nchc.dl.sourceforge.net/sourceforge/wxwindows/wxGTK-%{version}.tar.bz2
# This patch is also used in SFEwxwidgets.spec:
Patch1:                  wxgtk-01-sqrt.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsdl
Requires: SUNWmlib
BuildConflicts: SFEwxwidgets

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n wxGTK-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
%ifarch sparc
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

LDFLAGS="-L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib:/usr/sfw/lib" \
CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include" \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 \
            --with-sdl                       \
            --with-gtk                       \
            --enable-unicode                 \
            --with-gnomeprint
#            --with-opengl

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_bindir}
rm -f wx-config
ln -s ../lib/wx/config/gtk2-unicode-release-2.6 wx-config

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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bakefile

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEwxGTK
- change to root:bin to follow other JDS pkgs.
- get rid of -share pkg
- move stuff around between base and -devel
- add missing deps
- split l10n content into an -l10n subpkg
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
