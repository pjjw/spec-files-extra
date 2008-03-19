#
# spec file for package SFEinkscape
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): inkscape
#
%include Solaris.inc

Name:                    SFEinkscape
Summary:                 Inkscape - vector graphics editor
Version:                 0.45.1
Source:                  %{sf_download}/inkscape/inkscape-%{version}.tar.gz
URL:                     http://www.inkscape.org
Patch1:                  inkscape-01-no-ver-check.diff
Patch2:                  inkscape-02-aclocal.diff
Patch3:                  inkscape-03-isnormal.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWlibgc
Requires:      SUNWgnome-libs
Requires:      SFEgtkmm
Requires:      SFEglibmm
Requires:      SFEsigcpp
Requires:      SUNWlcms
BuildRequires: SFEgtkmm-devel
BuildRequires: SFEglibmm-devel
BuildRequires: SFEsigcpp-devel
BuildRequires: SUNWlibgc-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWlcms-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd inkscape-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# doesn't currently build with Forte
%if %cc_is_gcc
%else
echo this version of inkscape uses gcc specific code
#exit 1
%endif

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"

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

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/inkscape
%{_mandir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Feb  2 2008 - laca@sun.com
- bump to 0.45.1
- add patches aclocal.diff and isnormal.diff both fix build issues
- update %files lists - delete root pkg, add l10n pkg
* Tue Feb  6 2007 - damien.carbery@sun.com
- Bump to 0.45. Add Build/Requires SFElcms/-devel.
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
