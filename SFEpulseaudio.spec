#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name pulseaudio
%define src_url http://0pointer.de/lennart/projects/%{src_name}

Name:		SFEpulseaudio
Summary:	pulseaudio - stream audio to clients
Version:	0.9.5
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		pulseaudio-01-ioctl.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#TODO are dependencies complete? 
BuildRequires: SFElibsndfile-devel
BuildRequires: SUNWliboil-devel
BuildRequires: SFElibsamplerate-devel
Requires: SFElibsndfile
Requires: SUNWliboil
Requires: SFElibsamplerate

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#_XGP4_2 and __EXTENSIONS__ for rtp.c to find all typedefs
export CPPFLAGS="-D_XPG4_2 -D__EXTENSIONS__"

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags} -lxnet -lgobject-2.0"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libexecdir}/pulse*
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added ioctl patch and root package
* Tue May 22 2007 - Thomas Wagner
- Initial spec
