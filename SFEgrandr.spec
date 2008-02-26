#
# spec file for package SFEgrandr
#
# includes module(s): grandr
#
%include Solaris.inc

Name:                    SFEgrandr
Summary:                 GTK interface to the X Resize And Rotate (XRandR) extension
Version:                 0.1
Source:                  http://xorg.freedesktop.org/archive/individual/app/grandr-%{version}.tar.bz2
Patch1:                  grandr-01-gconf.diff
Patch2:                  grandr-02-desktop-file.diff
Patch3:                  grandr-03-iterator.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-base-libs
Requires:      SUNWxorg-clientlibs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWxorg-headers

%prep
%setup -q -n grandr-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"

#%define grandr_prefix          %{_basedir}/X11
#%define grandr_bindir          %{grandr_prefix}/bin
#%define grandr_libdir          %{grandr_prefix}/lib
#%define grandr_sysconfdir      %{_sysconfdir}


autoconf
./configure --prefix=%{_prefix}        \
            --bindir=%{_bindir}        \
            --libdir=%{_libdir}        \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp grandr.desktop $RPM_BUILD_ROOT%{_datadir}/applications

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%changelog
* Tue Feb 26 2008 - trisk@acm.jhu.edu
- Add patch3 from Debian - fixes long-standing crash
* Sun Sep 16 2007 - trisk@acm.jhu.edu
- Initial spec
