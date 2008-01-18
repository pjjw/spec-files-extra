#
# spec file for package SFEaspell
#
# includes module(s): aspell
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc

Name:          SFElibtunepimp
Summary:       Libtunepimp is a library for creating MusicBrainz enabled tagging applications.
Version:       0.5.3
License:       GPLv2
Source:        ftp://ftp.musicbrainz.org/pub/musicbrainz/libtunepimp-%{version}.tar.gz
Patch1:        libtunepimp-01-statvfs.diff
SUNW_BaseDir:  %{_prefix}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEreadline
BuildRequires: SFEreadline-devel
Requires:      SFEtaglib
BuildRequires: SFEtaglib-devel
Requires:      SFElibiconv
BuildRequires: SFElibiconv-devel
BuildRequires: SFElibmad-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWflac-devel
Requires:      SFElibmusicbrainz3
BuildRequires: SFElibmusicbrainz3-devel
Requires:      SUNWlexpt
Requires:      SUNWcurl
Requires:      SUNWzlib
Requires:      SFElibofa

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:  %{name}

%package encumbered
Summary:       %{summary} - support for encumbered codecs
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:  %{name}

%prep
%setup -q -n libtunepimp-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure \
    --prefix=%{_prefix} \
    --enable-shared=yes \
    --enable-static=no

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a

make
make all

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libtune*
%dir %attr (0755, root, other) %{_libdir}/tunepimp
%dir %attr (0755, root, other) %{_libdir}/tunepimp/plugins
%{_libdir}/tunepimp/plugins/flac.tpp
%{_libdir}/tunepimp/plugins/speex.tpp
%{_libdir}/tunepimp/plugins/tta.tpp
%{_libdir}/tunepimp/plugins/vorbis.tpp
%{_libdir}/tunepimp/plugins/wav.tpp
%{_libdir}/tunepimp/plugins/wv.tpp

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files encumbered
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/tunepimp
%dir %attr (0755, root, other) %{_libdir}/tunepimp/plugins
%{_libdir}/tunepimp/plugins/mp3.tpp
%{_libdir}/tunepimp/plugins/mpc.tpp
%{_libdir}/tunepimp/plugins/wma.tpp

%changelog
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Initial spec
