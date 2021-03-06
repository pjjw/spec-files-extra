#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFErecordmysolaris
Summary:             Recordmysolaris - Desktop recording tool
Version:             0.1
Source:              http://recordmysolaris.googlecode.com/files/recordmysolaris-%{version}.tar.gz
URL:                 http://code.google.com/p/recordmysolaris/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}_%{version}-build
BuildRequires:            SUNWogg-vorbis
BuildRequires:            SUNWlibtheora
BuildRequires:            oss

Requires:            oss
Requires:            SUNWxwplt
Requires:            SUNWogg-vorbis
Requires:            SUNWlibtheora

%include default-depend.inc

%prep
%setup -q -n recordmysolaris-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

aclocal
autoheader
automake --copy --add-missing
autoconf

./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --datadir=%{_datadir}               \
            --infodir=%{_infodir}


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/recordmysolaris
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Mon Aug 25 2008 - (andras.barna@gmail.com)
- Initial spec
