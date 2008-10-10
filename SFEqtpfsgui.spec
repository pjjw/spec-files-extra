#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include usr-gnu.inc

Name:                SFEqtpfsgui
Summary:             HDR imaging gui
Version:             1.9.1
Source:              %{sf_download}/qtpfsgui/qtpfsgui-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Patch1:			qtpfsgui-1.diff
%include default-depend.inc
%include perl-depend.inc

Requires: SFEexiv2-gpp
Requires: SUNWTiff
Requires: SFEfftw
Requires: SFEqt
Requires: SFEilmbase-gpp
Requires: SFEopenexr-gpp
BuildRequires: SFEfftw-devel
BuildRequires: SFEqt-devel
BuildRequires: SFEilmbase-gpp-devel
BuildRequires: SFEopenexr-gpp-devel
BuildRequires: SFEexiv2-gpp-devel


%prep
%setup -q -n qtpfsgui-%version
%patch1 -p0

export CC=gcc
export CXX=g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export CXXFLAGS="%{gcc_cxx_optflags}"


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl `/usr/bin/libart2-config --libs`"
export EXTRA_LIBS=`echo %_cxx_libdir|sed -e "s/\/gnu//"`
export PKG_CONFIG_PATH=$EXTRA_LIBS/pkgconfig:$PKG_CONFIG_PATH
export QMAKE_LFLAGS="-R$EXTRA_LIBS -L$EXTRA_LIBS"

extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"
sfw_prefix=`dirname %{sfw_bin}`

/usr/bin/qmake PREFIX=/usr/gnu LOCALSOFT=/usr/gnu QMAKE_LFLAGS="$QMAKE_LFLAGS"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/qtpfsgui
%{_datadir}/qtpfsgui/*

%changelog
* Fri Oct 10 2008 - markgraf@med.ovgu.de
- reworked to fetch g++ built ilmbase and openexr from
  /usr/lib/g++/<g++-version>
* Mon May 26 2008 - markgraf@med.ovgu.de
- Initial spec.
