#
# spec file for package SFEwebkit
#
# includes module(s): webkit
#
%include Solaris.inc

Name:                    SFEwebkit
Summary:                 WetKit, an open source web browser engine that's used by Safari, Dashboard, Mail, and many other OS X applications.
Version:                 38760
Source:                  http://builds.nightly.webkit.org/files/trunk/src/WebKit-r%{version}.tar.bz2
URL:                     http://www.webkit.org/

# owner:alfred date:2008-11-26 type:bug
Patch1:                  webkit-01-sun-studio-build-hack.diff
# owner:alfred date:2008-11-26 type:bug
Patch2:                  webkit-02-explicit-const.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEstdcxx
Requires: SUNWcurl
Requires: SUNWgnu-idn
Requires: SUNWgnome-base-libs
Requires: SUNWicu
Requires: SUNWlxml
Requires: SUNWopenssl
Requires: SUNWpr
Requires: SUNWsqlite3
Requires: SUNWtls
Requires: SUNWzlib
BuildRequires: SUNWgcc
BuildRequires: SFEstdcxx-devel

%prep
%setup -q -n %name-%version -c -a1
cd WebKit-r%version
%patch1 -p0
%patch2 -p0

%build

export SunStudioPath=/opt/SunStudioExpress
export CXXFLAGS="-features=zla -I/usr/stdcxx/include/ -library=no%Cstd"
export LDFLAGS="-L/usr/stdcxx/lib/ -lstd -L${SunStudioPath}/lib -lCrun -R/usr/stdcxx/lib/"

cd WebKit-r%version
./WebKitTools/Scripts/build-webkit --gtk

%install
rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%name-%version/WebKit-r%version/WebKitBuild/Release/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/gtk
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cp -R DerivedSources/*.h $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/
cp WebKit/gtk/webkit/webkitversion.h $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/gtk
cp WebKit/gtk/webkit-1.0.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cp .libs/libwebkit-1.0.so $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so.1.0.3
ln -s libwebkit-1.0.so.1.0.3 $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libwebkit*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_prefix}/include
%{_prefix}/include/*

%changelog
* Wed Nov 26 2008 - alfred.peng@sun.com
- Initial version
