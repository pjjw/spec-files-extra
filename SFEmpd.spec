#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# For the output section of ~/.mpdconf, this worked for me:
#
# audio_output {
#     type	"ao"
#     name      "libao audio device"
#     driver	"sun"
# }

%include Solaris.inc

Name:                SFEmpd
Summary:             Daemon for remote access music playing & managing playlists
Version:             0.12.0
Source:              http://www.musicpd.org/uploads/files/mpd-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibao
Requires: SFElibao

%prep
%setup -q -n mpd-%version

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
	    --enable-ao          \
	    --disable-id3

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

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
* Mon Nov 06 2006 - Eric Boutilier
- Fix attributes
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
