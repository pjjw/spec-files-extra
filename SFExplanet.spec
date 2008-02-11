# NOTE:
#
# You need to patch your Sun Studio compiler to be able to build this
# spec file.  Install 121018-07 or later, or
# apply patches/sun-studio-stlport4-fileno.diff
# to file SUNWspro/prod/include/CC/stlport4/stl/_stdio_file.h
# Here's how you do it:
#    $ su -
#    # cd /path/to/SUNWspro/prod/include/CC/stlport4/stl
#    # gpatch -p1 < /path/to/SFE/patches/sun-studio-stlport4-fileno.diff
#

#
# spec file for package SFExplanet
#
# includes module(s): xplanet
#
%include Solaris.inc

Name:                    SFExplanet
Summary:                 XPlanet
Version:                 1.2.0
Source:                  %{sf_download}/xplanet/xplanet-%{version}.tar.gz         
Patch1:                  xplanet-01-forte.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWTiff
Requires: SUNWfreetype2
Requires: SUNWgnome-base-libs
Requires: SUNWjpg
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWpng
Requires: SUNWxwrtl
Requires: SUNWzlib
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWpng-devel

%prep
%setup -q -n xplanet-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags -library=stlport4 -staticlib=stlport4"
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xplanet
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Fri Jun 30 2006 - laca@sun.com
- rename to SFExplanet
- delete -share subpkg
- update file attributes
* Tue Oct 25 2005 - glynn.foster@sun.com
- Initial spec
