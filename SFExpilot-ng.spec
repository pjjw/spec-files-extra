#
# spec file for package SFExpilot-ng
#
# includes module(s): xpilot-ng
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFExpilot-ng
Summary:                 XPilot - multi-player tactical manoeuvring game for X
Version:                 4.7.2
Source:                  %{sf_download}/xpilot/xpilot-ng-%{version}.tar.gz
Patch1:                  xpilot-ng-01-freealut.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image
BuildRequires: SFEopenal-devel
Requires: SFEopenal
BuildRequires: SFEfreealut-devel
Requires: SFEfreealut
Requires: SUNWzlib

%prep
%setup -q -n xpilot-ng-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-D__FUNCTION__=__func__ -D__unix__"
export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"

aclocal
libtoolize --copy --force 
automake -a -f
autoconf -f 
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --enable-sound

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xpilot-ng
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*

%changelog
* Sat Oct 27 2007 - trisk@acm.jhu.edu
- Initial spec
