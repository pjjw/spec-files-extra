#
# spec file for package SFEinkscape
#
# includes module(s): inkscape
#
%include Solaris.inc

Name:                    SFEinkscape
Summary:                 Inkscape - vector graphics editor
Version:                 0.44.1
Source:                  http://easynews.dl.sourceforge.net/sourceforge/inkscape/inkscape-%{version}.tar.gz
URL:                     http://www.inkscape.org
Patch1:                  inkscape-01-no-ver-check.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEhp-gc
Requires:      SUNWgnome-libs
Requires:      SFEgtkmm
Requires:      SFEglibmm
Requires:      SFEsigcpp
BuildRequires: SFEgtkmm-devel
BuildRequires: SFEglibmm-devel
BuildRequires: SFEsigcpp-devel
BuildRequires: SFEhp-gc-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWPython

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
cd inkscape-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# doesn't currently build with Forte
%if %cc_is_gcc
%else
echo this version of inkscape uses gcc specific code
exit 1
%endif

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
# we need -L/usr/lib so that /usr/lib/libgc.so is picked up instead of
# SUNWspro's own libgc.so
export LDFLAGS="%{_ldflags} -L/usr/lib"
cd inkscape-%{version}
glib-gettextize -f 
libtoolize --copy --force
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd inkscape-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/inkscape.schemas

%changelog
* Fri Oct 13 2006 - laca@sun.com
- bump to 0.44.1
* Thu Jul  6 2006 - laca@sun.com
- rename to SFEinkscape
- delete -share subpkg
- update file attributes
* Fri Mar 10 2006 - damien.carbery@sun.com
- Add Build/Requires for SUNWgtkmm, SUNWglibmm, SUNWsigcpp.
* Mon Jan 30 2006 - glynn.foster@sun.com
- Initial version
