#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEqt3
Summary:             Cross-platform development framework/toolkit (older version)
Version:             3.3.8
Source:              ftp://ftp.trolltech.com/qt/source/qt-x11-free-%{version}.tar.bz2

Patch1:             qt3-0001-dnd_optimization.patch
Patch2:             qt3-0002-dnd_active_window_fix.patch
#Patch3:             qt3-0003-qpixmap_mitshm.patch
Patch4:             qt3-0004-qpixmap_constants.patch
Patch5:             qt3-0005-qiconview-finditem.patch
Patch6:             qt3-0006-qiconview-rebuildcontainer.patch
Patch7:             qt3-0007-designer-deletetabs.patch
Patch8:             qt3-0008-fix_rotated_randr.diff
Patch9:             qt3-0009-qvaluelist-streaming-operator.patch
Patch10:             qt3-0010-dragobject-dont-prefer-unknown.patch
Patch11:             qt3-0011-qscrollview-windowactivate-fix.diff
Patch12:             qt3-0012-qclipboard_hack_80072.patch
Patch13:             qt3-0013-qiconview-rubber_on_move.diff
Patch14:             qt3-0014-png-gamma-fix.diff
Patch15:             qt3-0015-khotkeys_input_84434.patch
Patch16:             qt3-0016-qpopup_has_mouse.patch
Patch17:             qt3-0017-qpopup_ignore_mousepos.patch
Patch18:             qt3-0019-qscrollview-propagate-horizontal-wheelevent.patch
Patch19:             qt3-0020-auto-license.diff
Patch20:             qt3-0021-dont-use-includehints.diff
Patch21:             qt3-0022-q_export-visibility.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgccruntime
#FIXME: Requires: SUNWxorg-mesa
# Guarantee X/freetype environment concisely (hopefully):
Requires: SUNWGtku
Requires: SUNWxwplt
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
Requires: SFEcups
Requires: SFElibmng
BuildRequires: SFEcups-devel
BuildRequires: SUNWsqlite-devel
BuildRequires: SUNWsfwhea
BuildRequires: SUNWpostgr-devel
BuildRequires: SFElibmng-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n qt-x11-free-%version
%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

if [ "x`basename $CC`" != xgcc ]
then
	PLATFORM=solaris-cc
else
	PLATFORM=solaris-g++
fi
export CFLAGS="%optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include -I/usr/include/pgsql -I/usr/include/pgsql/server -I/usr/sfw/include/mysql"
#export CXXFLAGS=$CFLAGS

export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -L%{_builddir}/qt-x11-free-%{version}/lib"
export LD_LIBRARY_PATH="/usr/lib:/usr/X11/lib:/usr/gnu/lib:/usr/sfw/lib:%{_builddir}/qt-x11-free-%{version}/lib"

./configure -prefix %{_prefix} \
           -shared \
           -release \
           -platform ${PLATFORM} \
           -thread \
           -system-libpng \
           -system-libjpeg \
           -system-libmng \
           -system-zlib \
           -xft \
           -xcursor \
           -xrandr \
           -xrender \
           -plugin-sql-sqlite \
           -plugin-sql-mysql \
           -plugin-sql-psql \
           -dlopen-opengl \
           -no-exceptions \
           -docdir %{_docdir}/qt3 \
           -headerdir %{_includedir}/qt3 \
           -plugindir %{_libdir}/qt3/plugins \
           -datadir %{_datadir}/qt3 \
           -translationdir %{_datadir}/qt3/translations \
           -sysconfdir %{_sysconfdir} \
           -I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include -I/usr/sfw/include/mysql \
           -I/usr/include/pgsql -I/usr/include/pgsql/server \
           -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib \
           -L/usr/sfw/lib -R/usr/sfw/lib \
           -v

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Developing Qt apps needs a few .a libs
#
rm ${RPM_BUILD_ROOT}%{_libdir}/*.la

#
# Create a compatibility doc link
#
(cd ${RPM_BUILD_ROOT}%{_datadir}/qt3
  mkdir doc
  chmod 0755 doc
  cd doc
  ln -s ../../doc/qt3/html
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other)  %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, bin) %{_libdir}/qt3
%{_libdir}/qt3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.prl
%{_libdir}/lib*.a
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/qt3
%{_includedir}/qt3/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/qt3
%{_datadir}/qt3/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu Feb 15 2008 - Thomas Wagner
- add (Build-)Requires: SFElibmng(-devel)
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Create a compatibility doc link so that KDE and other software
- can find QT documentation.
- Do not remove static libs. Put them in devel package.
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Commented out patch 3 for now. Leaks memory like a sieve without
- showing any perceptible performance improvement.
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Fix Postgres dependency
- Fix copyright year
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Initial spec. Thanks to Stefan Teleman for the patches.
