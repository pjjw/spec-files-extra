#
# spec file for package SFEglibmm
#
# includes module(s): glibmm
#
%include Solaris.inc
%use glibmm = glibmm.spec

Name:                    SFEglibmm
Summary:                 glibmm - C++ Wrapper for the Glib2 Library
Version:                 %{glibmm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp
BuildRequires: SFEsigcpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%if %build_l10n
%package l10n
Summary:		 %{summary} - l10n files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires:		 %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%glibmm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"
export PERL_PATH=/usr/perl5/bin/perl
%glibmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%glibmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Remove m4, pm and extra_gen_defs directory
rm -rf $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc/m4
rm -rf $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc/pm
rm -rf $RPM_BUILD_ROOT%{_libdir}/libglibmm_generate_extra_defs*.so*
rm -rf $RPM_BUILD_ROOT%{_includedir}/glibmm-2.4/glibmm_generate_extra_defs

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || exit 0';
  echo 'rm -f %{_datadir}/icons/*/icon-theme.cache';
  echo 'ls -d %{_datadir}/icons/* | xargs -l1 /usr/bin/gtk-update-icon-cache'
) | $BASEDIR/lib/postrun -b -u -t 5 -c JDS
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/glibmm*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Feb 12 2008 - simon.zheng@sun.com
- Delete m4, pm and generate_extra_defs files.
* Mon Jau 28 2008 - simon.zheng@sun.com
- Split into SFEglibmm.spec and glibmm.spec.
- Change download URL to GNOME official website.
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.12.10
* Tue Apr 17 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.8.
* Fri Mar 16 2007 - laca@sun.com
- bump to 2.12.7
* Wed Jan 03 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12.4
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEglibmm
- update permissions
- bump to 2.10.4
* Fri May 12 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Fri Mar 10 2006 - damien.carbery@sun.com
- Bump to 2.10.0.
* Thu Nov 17 2005 - laca@sun.com
- create
