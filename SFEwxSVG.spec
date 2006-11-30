#
# spec file for package SFEwxSVG
#
# includes module(s): SFEwxSVG
#
%include Solaris.inc

Name:                    SFEwxSVG
Summary:                 wxGTK a C++ library to create, manipulate and render SVG files
Version:                 1.0.0.7
%define tarball_version 1.0b7
Source:                  http://nchc.dl.sourceforge.net/sourceforge/wxsvg/wxsvg-%{tarball_version}_1.tar.gz
Patch1:			 wxsvg-01-sqrt.diff
Patch2:                  wxsvg-02-pango-deprecated.diff
Patch3:                  wxsvg-03-1586173-append-void.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
%if %(pkginfo -q SFEwxwidgets && echo 1 || echo 0)
Requires: SFEwxwidgets
%else
Requires: SFEwxGTK
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n wxsvg-%tarball_version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
%ifarch sparc
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

LDFLAGS="-L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib:/usr/sfw/lib" \
CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include" \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Nov 28 2006 - laca@sun.com
- make it work with either SFEwxwidgets or SFEwxGTK
- change version to numeric
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
