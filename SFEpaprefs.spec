#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


%include Solaris.inc

%define SUNWgtkmm      %(/usr/bin/pkginfo -q SUNWgtkmm && echo 1 || echo 0)



Name:                SFEpaprefs
Summary:             paprefs - PulseAudio Preferences Control
Version:             0.9.5
Source:              http://0pointer.de/lennart/projects/paprefs/paprefs-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc


#TODO are dependencies complete? 
%if %SUNWgtkmm
BuildRequires: SUNWgtkmm-devel
%else
BuildRequires: SFEgtkmm-devel
%endif
BuildRequires: SFEgconfmm-devel
BuildRequires: SFElibglademm-devel
BuildRequires: SFEpulseaudio-devel
BuildRequires: SFElynx
BuildRequires: SFElynx
%if %SUNWgtkmm
Requires: SUNWgtkmm
%else
Requires: SFEgtkmm
%endif
Requires: SFEgconfmm
Requires: SFElibglademm
Requires: SFEpulseaudio
Requires: SFElynx
Requires: SFElynx


#%package 
#Name:			 SFElibpaprefs
#Summary:                 %{summary} - library files
#SUNW_BaseDir:            %{_basedir}
#%include default-depend.inc
#Requires: %name



%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n paprefs-%version
#%patch1 -p1
#%patch2 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#_XGP4_2 and __EXTENSIONS__ for rtp.c to find all typedefs
export CFLAGS="-D_XPG4_2 -D__EXTENSIONS__ %optflags"
#export LDFLAGS="%{_ldflags} -lxnet -lgobject-2.0"
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

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/paprefs
%{_datadir}/paprefs/*





%changelog
* Fri Sep 05 2008 - Thomas Wagner
- switch between SUNWgtkmm and SFEgtkmm depending on availability
* Tue May 23 2007 - Thomas Wagner
- Initial spec
