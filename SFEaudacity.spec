#
# spec file for package SFEaudacity
#
# includes module(s): audacity
#
%include Solaris.inc

%define with_libmad %(pkginfo -q SFElibmad && echo 1 || echo 0)
%define with_libtwolame %(pkginfo -q SFElibtwolame && echo 1 || echo 0)
%define with_wxw_gcc %(pkginfo -q SFEwxwidgets-gnu && echo 1 || echo 0)
%define with_gnu_gettext %(pkginfo -q SFEgettext && echo 1 || echo 0)

%define	src_name audacity
%define	src_url	http://downloads.sourceforge.net/audacity

Name:                SFEaudacity
Summary:             Free, Cross-Platform Sound Editor
Version:             1.3.4
Source:              %{src_url}/%{src_name}-src-%{version}.tar.bz2
# bug 1910678
Patch1:		     audacity-01-solaris.diff
Patch2:		     audacity-02-float.diff
# bug 1910681
Patch3:		     audacity-03-alloca.diff
Patch4:		     audacity-04-fixconfigure.diff
# bug 1910685
Patch5:              audacity-05-fixsed.diff
# bug 1910687
Patch7:              audacity-07-nowall.diff
# bug 1910688
Patch9:              audacity-09-fixmatrix.diff
# bug 1910699
Patch10:             audacity-10-addgtklibs.diff
# bug 1910700
Patch11:             audacity-11-fix-pa-makefile.diff
Patch12:             audacity-12-no-pa-threads.diff
Patch13:             audacity-13-locale.diff
# bug 1911499
Patch14:             audacity-14-AudioIO.diff
Patch15:             audacity-15-importmp3.diff
# This patch is wrong, but it gets the code to compile.
Patch16:             audacity-16-fixvamp.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibsamplerate-devel
Requires: SFElibsamplerate
BuildRequires: SFEportaudio-devel
Requires: SFEportaudio
BuildRequires: SFEladspa-devel
Requires: SFEladspa
BuildRequires: SFEsoundtouch-devel
Requires: SFEsoundtouch

# Check whether the user has installed the Sun Studio or GCC
# version of wxWidgets, and build with GCC if using the GCC
# version
%if %with_wxw_gcc
BuildRequires: SFEgcc
BuildRequires: SFEwxwidgets-gnu-devel
Requires: SFEwxwidgets-gnu
%else
BuildRequires: SFEwxwidgets-devel
Requires: SFEwxwidgets
%endif

# If building with libmad, then also require id3tag.  If
# building with the GCC wxwidgets, then also require the
# GCC version of libid3tag.
#
%if %with_libmad
BuildRequires: SFElibmad-devel
Requires: SFElibmad

%if %with_wxw_gcc
BuildRequires: SFElibid3tag-gnu-devel
Requires: SFElibid3tag-gnu
%else
BuildRequires: SFElibid3tag-devel
Requires: SFElibid3tag
%endif
%endif

# If twolame is installed, build with it.
%if %with_libtwolame
BuildRequires SFEtwolame-devel
Requires SFEtwolame
%endif

%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n %{src_name}-src-%{version}-beta
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

# Sun Studio specific patches
#
%if %with_wxw_gcc
%else
%patch4 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%endif

# If using GNU Gettext, don't need this patch
#
#%if %with_gnu_gettext
#%else
#%patch13 -p1
#%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %with_wxw_gcc
%if %debug_build
export CFLAGS="-g"
AU_DEBUG_CONFIG=-enable-debug --enable-debug-output
%else
export CFLAGS="-O4"
AU_DEBUG_CONFIG=-disable-debug
%endif
%endif

export CPPFLAGS="-I/usr/gnu/include -I/usr/X11/include -I/usr/sfw/include"
export PATH=/usr/gnu/bin:$PATH
export LDFLAGS="-L/usr/gnu/lib -L/usr/X11/lib -R/usr/gnu/lib -R/usr/X11/lib -R/usr/sfw/lib"
%if %with_wxw_gcc
export CC=gcc
export CXX=g++
%endif
CFLAGS="$CFLAGS -fPIC -DPIC -fno-omit-frame-pointer"
CXXFLAGS="$CFLAGS -fPIC -DPIC -fno-omit-frame-pointer"

%if %with_libmad
AU_LIBMAD_CONFIG="--with-libmad"
%else
AU_LIBMAD_CONFIG="--without-libmad"
%endif

%if %with_libtwolame
AU_LIBTWOLAME_CONFIG="--with-libtwolame"
%else
AU_TWOLAME_CONFIG="--without-libtwolame"
%endif

# Must run autoconf in portaudio-v19 code since we patch
# configure.in.
#
cd lib-src/portaudio-v19
autoconf -f
cd ../..

libtoolize -f -c
aclocal
autoconf -f
autoheader

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --datadir=%{_datadir}       \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir}         \
            --with-ladspa               \
            $AU_DEBUG_CONFIG		\
            $AU_LIBMAD_CONFIG		\
            $AU_LIBTWOMAD_CONFIG	\
            --without-quicktime

%if %with_wxw_gcc
# /usr/gnu/bin/gcc is using gnu ld....
perl -pi -e 's/-M ...wl./--version-script=/' lib-src/portaudio-v19/libtool
perl -pi -e 's/-Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect//' src/Makefile
perl -pi -e 's/-Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect//' tests/Makefile
%endif

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/audacity
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (-, root, root) %{_datadir}/mime
%attr (-, root, root) %{_datadir}/mime/*

%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Mon Mar 18 2008 - brian.cameron@sun.com
- Bump to 1.3.4.  Many changes to the patches to get this new version
  working.  SoundTouch was removed from the audacity release, so I added
  a separate spec-file to build SoundTouch, and made this package depend
  on it.
* Sun Mar  9 2008 - brian.cameron@sun.com
- Bump to 1.3.3.  Add new patches to allow building with Sun Studio.
  Fix so that libmad, libid3tag, and libtwolame support is only included if
  they are already installed, so this spec doesn't build with any encumbered
  dependencies unless they are already installed on the system.  Also
  add patch to allow building without GNU gettext if it is not alrady
  installed on the system.
* Tue Feb 12 2008 - pradhap (at) gmail.com
- Fix links
* Sat Sep 22 2007 - dougs@truemail.co.th
- Initial spec
