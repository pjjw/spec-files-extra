#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


%include Solaris.inc

Name:                SFEpulseaudio
Summary:             pulseaudio - stream audio to clients
Version:             0.9.5
Source:              http://0pointer.de/lennart/projects/pulseaudio/pulseaudio-%{version}.tar.gz

#SUNW_BaseDir:        %{_basedir}
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

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


%prep
%setup -q -n pulseaudio-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#_XGP4_2 and __EXTENSIONS__ for rtp.c to find all typedefs
export CFLAGS="-D_XPG4_2 -D__EXTENSIONS__ %optflags"
export LDFLAGS="%{_ldflags} -lxnet -lgobject-2.0"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}



make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*
%defattr (-, root, bin)
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/pulse*
%{_libexecdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*



%changelog
* Tue May 22 2007 - Thomas Wagner
- Initial spec
