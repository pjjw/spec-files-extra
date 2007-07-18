#
# spec file for package SFEpigment
#
# includes module(s): pigment
#
# Note that the 0.3.0.1 version is building "make dist" from SVN head.
# This latest version works on Solaris, whereas the last released version
# does not.  When 0.3.x actually comes out, then this will be a bit easier
# to build.  But for those who want to try out pigment right now, this
# spec file does work.
#
%define name pigment
%define version 0.3.0.1
%define pythonver 2.4

%include Solaris.inc

Summary:         Python user interface library with embedded multimedia
Name:            SFE%{name}
Version:         %{version}
URL:             https://core.fluendo.com/pigment/trac
Source0:         http://elisa.fluendo.com/static/download/pigment/pigment-%{version}.tar.bz2
Patch1:          pigment-01-noMacOS.diff
Patch2:          pigment-02-fixconfigure.diff
SUNW_BaseDir:    %{_basedir}
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWPython-devel
BuildRequires:   SUNWgnome-common-devel
BuildRequires:   SUNWgnome-media-devel
BuildRequires:   SUNWgnome-base-libs-devel
BuildRequires:   SUNWgnome-python-libs
BuildRequires:   SFEgst-python

%include default-depend.inc

%description
Pigment is a Python library designed to easily build user interfaces 
with embedded multimedia. Its design allows to use it on several 
platforms, thanks to a plugin system allowing to choose the underlying 
graphical API. Pigment is the rendering engine of Elisa, the Fluendo 
Media Center project.

%package devel
Group: Development/Python
Summary: Development headers for Pigment

%description devel
Pigment is a Python library designed to easily build user interfaces 
with embedded multimedia. Its design allows to use it on several 
platforms, thanks to a plugin system allowing to choose the underlying 
graphical API. Pigment is the rendering engine of Elisa, the Fluendo 
Media Center project.

%prep
%setup -q -n pigment-%version
%patch1 -p1 
%patch2 -p1 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal $ACLOCAL_FLAGS -I ./common/m4
gtkdocize
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
gmake 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm -r $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -r $RPM_BUILD_ROOT/%{_libdir}/pigment-0.3/*.la
rm -r $RPM_BUILD_ROOT/%{_libdir}/pigment-0.3/gstreamer/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python%{pythonver}/vendor-packages/*.la

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/pigment-0.3
%{_libdir}/python%{pythonver}/vendor-packages/_pgmmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/pgm
%{_libdir}/python%{pythonver}/vendor-packages/pypgmtools

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
#%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
#%{_datadir}/gtk-doc/html/*

%changelog
* Tue Jul 10 2007 Brian Cameron <brian.cameron@sun.com>
- Create spec file.
