#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


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

##FIXME##
#BuildRoot:           %{_tmppath}/%{name}-%{version}-build
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
##FIXME## include test for 64-bit libmng, then build in 64-bit
Requires: SFElibmng
BuildRequires: SFEcups-devel
##TODO##BuildRequires: SUNWsqlite-devel
BuildRequires: SUNWsfwhea
##FIXME## include test for 64-bit libpq.so, then build in 64-bit with postgres
#BuildRequires: SUNWpostgr-devel
BuildRequires: SUNWpostgr-82-devel
##FIXME## include test for 64-bit libmng.so, otherwise no qt3 64-bit possible
BuildRequires: SFElibmng-devel


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

# %{libdiradd} defines as /amd64 or as /sparcv9

export LDLIBS32="-L/usr/X11/lib             -R/usr/X11/lib             -L/usr/gnu/lib             -R/usr/gnu/lib             -L/usr/sfw/lib             -R/usr/sfw/lib             -L/usr/postgres/8.2/lib             -R/usr/postgres/8.2/lib"
#-L%{_builddir}/qt-x11-free-%{version}/lib        

export LDLIBS64="-L/usr/X11/lib%{libdiradd} -R/usr/X11/lib%{libdiradd} -L/usr/gnu/lib%{libdiradd} -R/usr/gnu/lib%{libdiradd} -L/usr/sfw/lib%{libdiradd} -R/usr/sfw/lib%{libdiradd} -L/usr/postgres/8.2/lib%{libdiradd} -R/usr/postgres/8.2/lib%{libdiradd}"
#-L%{_builddir}/qt-x11-free-%{version}/lib%{libdiradd}

export CFLAGSPG="-I/usr/postgres/8.2/include -I/usr/postgres/8.2/include/server"
##FIXME## mysql includes once 64-bit client lib is available
export CFLAGSQT="-I/usr/X11/include -I/usr/gnu/include -I/usr/sfw/include -I/usr/sfw/include/mysql"


#used at build-time:
export LD_LIBRARY_PATH="/usr/lib%{libdiradd}:/usr/X11/lib%{libdiradd}:/usr/gnu/lib%{libdiradd}:/usr/sfw/lib%{libdiradd}:%{_builddir}/%{name}-%{version}/%{bld_arch}/qt-x11-free-%{version}/lib"

%if %{opt_arch64}
  export LDLIBS=${LDLIBS64}
%elseif
  export LDLIBS=${LDLIBS32}
%endif


export QTDIR="%{_builddir}/%{name}-%{version}/%{bld_arch}/qt-x11-free-%{version}/lib"
export CFLAGS="%optflags ${CFLAGSQT} ${CFLAGSPG} ${LDLIBS}"
export CXXFLAGS="%cxx_optflags ${CFLAGSQT} ${CFLAGSPG} ${LDLIBS}"
export LDFLAGS="%{_ldflags} ${LDLIBS} "


##FIXME## 64-bit libs sqlite und mysql missing in 64-bit builds
echo "_prefix " %{_prefix}
echo "_bindir " %{_bindir}
echo "_libdir " %{_libdir}
echo "plugindir   " %{_libdir}/plugins
echo "_includedir " %{_includedir}
echo "_datadir " %{_datadir}
echo "_sysconfdir " %{_sysconfdir}
echo "translationdir " %{_datadir}/%{qt_subdir}/translations
echo "_docdir " %{_docdir}

 ./configure -prefix %{_prefix} \
             -bindir %{_bindir} \
             -libdir %{_libdir} \
             -plugindir %{_libdir}/plugins \
             -headerdir %{_includedir} \
             -datadir %{_datadir}/%{qt_subdir} \
             -sysconfdir %{_sysconfdir} \
             -translationdir %{_datadir}/%{qt_subdir}/translations \
             -docdir %{_docdir}/%{qt_subdir} \
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
%if %{opt_arch64}
%elseif
             -plugin-sql-mysql \
             -plugin-sql-sqlite \
%endif
             -plugin-sql-psql \
             -dlopen-opengl \
             -no-exceptions \
             ${CFLAGSPG} \
             ${CFLAGSQT} \
             ${LDLIBS} \
             -lCrun -lCstd \
             -v


gmake -j$CPUS

%install

gmake install INSTALL_ROOT=$RPM_BUILD_ROOT

##FIXME## is this what we want
ls -1 $RPM_BUILD_ROOT%{_libdir}/*.la >/dev/null 2>&1  && rm $RPM_BUILD_ROOT%{_libdir}/*.la
##FIXME## is this what we want
#contained in the devel package  rm $RPM_BUILD_ROOT%{_libdir}/*.prl

##FIXME## are these symolic links needed in a normal install? (note: points to a directory in the build tree)
#/usr/qtgcc/3/share/qtgcc/3/mkspecs/solaris-g++-64/solaris-g++-64
#/usr/qtgcc/3/share/qtgcc/3/mkspecs/solaris-g++/solaris-g++
(echo "deleting symlinks to build tree..."; cd  $RPM_BUILD_ROOT%{_datadir}/%{qt_subdir}/mkspecs/default && find . -type l -exec rm {} \; -print)


%clean
rm -rf $RPM_BUILD_ROOT



%changelog
* Sun Apr 13 2008 - Thomas Wagner
- experiment with new path layout
- switches to build SunStudio and gcc based packages
  use: pkgtool build SFEqt3.spec  *or* CC=gcc CXX=g++ pkgtool buils SFEqt3.spec (-> SFEqtgcc is the pkgname)
* Sat Mar 22 2008 - Thomas Wagner
- move qt3 _basedir into /usr/qt/3 (%{qt_subdir}) to avoid conflicts with qt4
  and follow filestandards as close as possible (please report otherwise)
* Mon Mar 17 2008 - Thomas Wagner
- build 32/64-bit with postgres-lib (note: mysql/sqlite only in 32bit)
* Thu Feb 15 2008 - Thomas Wagner
- add (Build-)Requires: SFElibmng(-devel) (needed in 64-bit)
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
