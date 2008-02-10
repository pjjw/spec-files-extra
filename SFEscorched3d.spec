#
# spec file for package SFEscorched3d.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

Name:                    SFEscorched3d
Summary:                 A 3D game based on the classic DOS game, Scorched Earth
Version:                 41.3
Source:                  http://downloads.sourceforge.net/scorched3d/Scorched3D-%{version}-src.tar.gz
Patch1:                  scorched3d-01-securid.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-devel
Requires: SFEsdl
BuildRequires:	SFEsdl-mixer-devel
Requires:	SFEsdl-mixer
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SFEopenal
BuildRequires: SFEopenal-devel
Requires: SUNWfreetype2
Requires: SFEfftw
BuildRequires: SFEfftw-devel
Requires: SFEwxwidgets-gnu
BuildRequires: SFEwxwidgets-gnu-devel
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SFEsdl-net
BuildRequires: SFEsdl-net-devel

%prep
%setup -q -n scorched
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-D__C99FEATURES__"
export CFLAGS="%optflags -I%{sfw_inc} -I%{gnu_inc} -std=c99"
export ACLOCAL_FLAGS="-I m4"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="-Wl,-zignore -Wl,-zcombreloc -Wl,-zdirect -lsocket -lnsl %{sfw_lib_path} %{gnu_lib_path}"
export LIBS=${LDFLAGS}
gnu_prefix=`basename %{gnu_bin}`

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --datadir=%{_datadir}		\
            --disable-nls			\
            --enable-shared			\
	    --disable-static			\
            --with-sdl-prefix=${gnu_prefix}

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
