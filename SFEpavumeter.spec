#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


%include Solaris.inc

Name:                SFEpavumeter
Summary:             pavumeter - PulseAudio Volume Meter, a simple GTK volume meter for the PulseAudio sound server
Version:             0.9.2
Source:              http://0pointer.de/lennart/projects/pavumeter/pavumeter-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc


#TODO are dependencies complete? 
BuildRequires: SFEgtkmm-devel
BuildRequires: SFEpulseaudio-devel
BuildRequires: SFElynx
BuildRequires: SFElynx
Requires: SFEgtkmm
Requires: SFEpulseaudio
Requires: SFElynx
Requires: SFElynx


#%package 
#Name:			 SFElibpavumeter
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
%setup -q -n pavumeter-%version
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



%changelog
* Tue May 23 2007 - Thomas Wagner
- Initial spec
