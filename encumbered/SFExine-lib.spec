#
# spec file for package SFExine-lib
#
# includes module(s): xine-lib
#

%include Solaris.inc
%use mplayer = SFEmplayer.spec

Name:         SFExine-lib
License:      GPL
Group:        System/Libraries
Version:      1.1.4
Summary:      xine-lib - the core engine of the xine video player
Source:       http://easynews.dl.sourceforge.net/sourceforge/xine/xine-lib-%{version}.tar.gz
Patch1:       xine-lib-01-sysi86.diff
Patch2:       xine-lib-02-asm-pic.diff
Patch3:       xine-lib-03-gettext.diff
Patch4:       xine-lib-04-hal-support.diff
Patch5:       xine-lib-05-buildfix.diff
Patch6:       xine-lib-06-oss.diff	
URL:          http://xinehq.de/index.php/home
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-vfs-devel
Requires: SUNWgnome-vfs
BuildRequires: SFEaalib-devel
Requires: SFEaalib
BuildRequires: SUNWxorg-headers
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWlibtheora-devel
Requires: SUNWlibtheora
Requires: SUNWsmbau
BuildRequires: SFElibcdio-devel
Requires: SFElibcdio
BuildRequires: SFElibmng-devel
Requires: SFElibmng
BuildRequires: SFElibdvdnav-devel
Requires: SFElibdvdnav
BuildRequires: SFElibmad-devel
Requires: SFElibmad
Requires: SUNWhal

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
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
%setup -q -n xine-lib-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

glib-gettextize --force
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I m4
autoheader
automake -a -c -f 
autoconf
export CXX=/usr/sfw/bin/gcc
export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4 -fPIC -DPIC -I/usr/X11/include -I/usr/openwin/include -D_LARGEFILE64_SOURCE -I/usr/sfw/include -mcpu=pentiumpro -mtune=pentiumpro -msse2 -mfpmath=sse "
export LDFLAGS="%{_ldflags} -L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib"
./configure --prefix=%{_prefix} \
            --with-w32-path=%{mplayer.codecdir} \
            --with-external-libmad \
            --with-external-dvdnav \
            --disable-opengl
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

for doc in README.dvb README.dxr3 README.freebsd README.irix README.opengl \
            README.solaris README.syncfb README; do
  rm $RPM_BUILD_ROOT%{_datadir}/doc/xine-lib/$doc
done

# the xv video driver causes a deadlock in 1.1.3
# still works in 1.1.2, but the problem doesn't seem to be in the xv
# driver itself; still investigating
#
# More info from Bernd Markgraf: the deadlock only happens starting from
# snv_51.
#
# Even more info from Alan Coopersmith: this is caused by libXv.so.1
# build issues in snv_51 to snv_44 (bugster 6494070)
snv_build=`uname -v`
case "$snv_build" in
    snv_5[1-6])
    echo "Deleting the XV video out plugin because it causes a deadlock in"
    echo "snv_51 to snv_55.  Please upgrade to snv_56 or later"
    rm $RPM_BUILD_ROOT%{_libdir}/xine/plugins/*/xineplug_vo_out_xv.so
    ;;
esac

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%{_libdir}/xine
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xine

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/xine-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Feb 26 2007 - markgraf@med.ovgu.de
- fix xine-lib-04-hal-support
  xineplug_inp_dvd.so needs to link LIBHAL_LIBS
* Fri Feb 23 2007 - markgraf@med.ovgu.de
- add patch to fix two hiccups with OSS 4.0x 
  (SOUND_PCM_SETFMT/SNDCTL_DSP_SETFMT and 
   SOUND_PCM_WRITE_RATE/SNDCTL_DSP_SPEED)
* Wed Feb 21 2007 - laca@sun.com
- re-enable the Xv video out plugin on snv_56 and later as libXv.so was fixed.
- bump to 1.1.4
- merge patches
- add patch buildfix.diff that adds a missing -I to a makefile
- disable the opengl plugin because it breaks the build -- need to investigate
  more
* Tue Jan 23 2007 - laca@sun.com
- move skins and plugins to base pkg from devel
* Sun Jan 21 2007 - laca@sun.com
- add missing defattr tag to %files
* Sun Jan  7 2007 - laca@sun.com
- create