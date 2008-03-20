#
# spec file for package SFEpigment-python
#
# includes module(s): pigment-python
#
%define name pigment-python
%define version 0.3.3
%define pythonver 2.4

%include Solaris.inc

Summary:         Python interfaces for pigment
Name:            SFE%{name}
Version:         %{version}
URL:             https://core.fluendo.com/pigment/trac
Source0:         http://elisa.fluendo.com/static/download/pigment/pigment-python-%{version}.tar.bz2
SUNW_BaseDir:    %{_basedir}
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWPython-devel
BuildRequires:   SUNWgnome-common-devel
BuildRequires:   SUNWgnome-media-devel
BuildRequires:   SUNWgnome-base-libs-devel
BuildRequires:   SUNWgnome-python-libs-devel
BuildRequires:   SUNWgst-python
BuildRequires:   SFEpigment-devel
Requires:        SUNWgnome-base-libs
Requires:        SUNWgnome-media
Requires:        SUNWgnome-python-libs
Requires:        SFEpigment
Requires:        SUNWgst-python

%include default-depend.inc

%description
Python interfaces for pigment.  Pigment is a library designed to easily
build user interfaces with embedded multimedia. Its design allows to use
it on several platforms, thanks to a plugin system allowing to choose
the underlying graphical API. Pigment is the rendering engine of Elisa,
the Fluendo Media Center project.

%prep
%setup -q -n pigment-python-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal $ACLOCAL_FLAGS
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

rm -f $RPM_BUILD_ROOT/%{_libdir}/python%{pythonver}/vendor-packages/*.la

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/_pgmgtkmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/_pgmmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/pgm
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pigment-python

%changelog
* Wed Mar 19 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.3
* Wed Feb 06 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.2.
* Wed Jan 16 2008 Brian Cameron  <brian.cameron@sun.com>
- Created.
