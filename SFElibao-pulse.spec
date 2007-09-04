#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


%include Solaris.inc

Name:                SFElibao-pulse
Summary:             libao-pulse - PulseAudio Plugin for the standard libao Audio Library (spec-files-extra-Version)
Version:             0.9.3
Source:              http://0pointer.de/lennart/projects/libao-pulse/libao-pulse-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc


%description
libao-pulse - PulseAudio Plugin to libao Framework. Used primarily to redirect Audio to/from the pulseaudio-framework from libao-capable programs writing/reading to/from the standard libao Audio Library (spec-files-extra-Version)


#TODO are dependencies complete? 
BuildRequires: SFEpulseaudio-devel
BuildRequires: SFElibao-devel
Requires: SFEpulseaudio
Requires: SFElibao


%prep
%setup -q -n libao-pulse-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-D_XPG4_2 -D__EXTENSIONS__ %optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}



make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT/%{_libdir}/ao/plugins-2/*\.a
rm -r $RPM_BUILD_ROOT/%{_libdir}/ao/plugins-2/*\.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/ao




%changelog
* Tue Sep 04 2007 - Thomas Wagner
- Initial spec
