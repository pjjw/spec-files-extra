#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc


Name:                SFEakode
Summary:             A simple audio decoding framework used by kdemultimedia
Version:             2.0.2
Source:              http://www.kde-apps.org/CONTENT/content-files/30375-akode-%{version}.tar.bz2
URL:                 http://www.kde-apps.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWflac
Requires: SUNWlibms
Requires: SUNWspeex
BuildRequires: SUNWspeex-devel
Requires: SUNWlibtool
Requires: SUNWaudh
BuildRequires: SFEffmpeg-devel
BuildRequires: SFElibmad-devel
BuildRequires: oss
Requires: SFEjack
BuildRequires: SFEjack-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWogg-vorbis-devel
Requires: SUNWspeex-devel
Requires: SFEffmpeg-devel
Requires: SFElibmad-devel
Requires: oss
Requires: SFEjack-devel

%package encumbered
Summary:                 %{summary} - support for encumbered codecs
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n akode-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="-D__EXTENSIONS__ -fPIC"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --enable-shared=yes \
            --enable-static=no \
            --enable-final

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Do not remove .la files
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Generate libraries list since we have to separately
# package encumbered codecs.
#
(cd ${RPM_BUILD_ROOT}; find ./%{_libdir}/* | \
    egrep -v "mpeg" | sed 's/^\.\///' \
    > %{_builddir}/akode-%version/akode_libfiles)


%clean
rm -rf $RPM_BUILD_ROOT

%files -f akode_libfiles
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files encumbered
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*mpeg*

%changelog
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Updated dependencies of devel package
* Sat Jan 19 2008 - moinak.ghosh@sun.com
- Do not include default CFLAGS and LDFLAGS. Screws up akode.
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Change summary line for encumbered package
* Wed Jan 17 2008 - moinak.ghosh@sun.com
- Initial spec
