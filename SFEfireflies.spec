#
# spec file for package SFEfireflies
#
# includes module(s): fireflies
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFEfireflies
Summary:                 Fireflies screensaver
URL:                     http://somewhere.fscked.org/fireflies/
Version:                 2.07
Source:                  http://somewhere.fscked.org/fireflies/fireflies-%{version}.tar.gz
Patch1:                  fireflies-01-sunpro.diff
Patch2:                  fireflies-02-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif

%prep
%setup -q -n fireflies-%version
gunzip -c libgfx-1.0.1.tar.gz | tar xf -
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -I/usr/X11/include"
export CXXFLAGS="%cxx_optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"
export LIBS="$LDFLAGS -lX11"

cd libgfx
aclocal
autoconf -f
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}

cd src
make -j$CPUS

cd ../..
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11/lib/xscreensaver/hacks
mv $RPM_BUILD_ROOT%{_prefix}/X11R6/lib/xscreensaver/* $RPM_BUILD_ROOT%{_prefix}/X11/lib/xscreensaver/hacks/
# this already exists
#mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11/lib/xscreensaver/config/control-center-2.0
#mv $RPM_BUILD_ROOT/fireflies.xml $RPM_BUILD_ROOT%{_prefix}/X11/lib/xscreensaver/config/control-center-2.0/fireflies.xml
rm -f $RPM_BUILD_ROOT/fireflies.xml
rm -rf $RPM_BUILD_ROOT%{_prefix}/X11R6


%clean

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/xscreensaver/hacks
%{_prefix}/X11/lib/xscreensaver/hacks/*
#%dir %attr (0755, root, other) %{_prefix}/X11/lib/xscreensaver/config/control-center-2.0
#%{_prefix}/X11/lib/xscreensaver/config/control-center-2.0/*

%changelog
* Fri Mar 07 2008 - trisk@acm.jhu.edu
- Initial spec
