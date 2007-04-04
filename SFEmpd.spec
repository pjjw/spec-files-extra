#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


# For the output section of ~/.mpdconf or /etc/mpd.conf try:
#
# audio_output {
#     type	"ao"
#     name      "libao audio device"
#     driver	"sun"
# }

%include Solaris.inc

Name:                SFEmpd
Summary:             Daemon for remote access music playing & managing playlists
Version:             0.12.2
Source:              http://www.musicpd.org/uploads/files/mpd-%{version}.tar.bz2
Patch1:              mpd-01-include-ao-mpdconf.example.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibao-devel
BuildRequires: SFElibmpcdec-devel
BuildRequires: SFElibmad-devel
BuildRequires: SFEfaad2-devel
BuildRequires: SFElibid3tag-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWflac-devel
Requires: SFElibao
Requires: SFElibmpcdec
Requires: SFElibmad
Requires: SFEfaad2
Requires: SFElibid3tag
Requires: SFEid3lib
Requires: SUNWogg-vorbis
Requires: SUNWgnome-audio
Requires: SUNWflac

%prep
%setup -q -n mpd-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

# Note: mp3 decoding and id3tag support is not configured 
# in here (it probably should be though)

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
	    --enable-ao          

#	    --disable-id3

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'retval=0';
  echo '[ -f /etc/mpd.conf ] || cp -p $PKG_INSTALL_ROOT%{_datadir}/doc/mpd/mpdconf.example $PKG_INSTALL_ROOT%{_sysconfdir}/mpd.conf'
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE



%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mpd
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/mpd.1
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/mpd.conf.5
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Wed Apr 04 2007 - Thomas Wagner
- bump to 0.12.2
- added dependencies
- modified configuration note to name /etc/mpd.conf
- copy patched mdconf.example to /etc/mpd.conf
- re-add id3 tags (untested)
* Mon Nov 06 2006 - Eric Boutilier
- Fix attributes
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
