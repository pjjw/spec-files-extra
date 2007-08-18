#
# spec file for package SFEgobby
#
# includes module(s): gobby
#
%include Solaris.inc

Name:                    SFEgobby
Summary:                 Gobby - collaborative editor
Version:                 0.4.4
%define tarball_version  0.4.4
Source:                  http://releases.0x539.de/gobby/gobby-%{tarball_version}.tar.gz
Patch1:                  gobby-01-prototype.diff
Patch2:                  gobby-02-const.diff
Patch3:                  gobby-03-auto_ptr.diff
URL:                     http://gobby.0x539.de/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs
Requires:      SFEgtkmm
Requires:      SFEglibmm
Requires:      SFEsigcpp
Requires:      SFElibxmlpp
Requires:      SFEnet6
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEgtkmm-devel
BuildRequires: SFEglibmm-devel
BuildRequires: SFEsigcpp-devel
BuildRequires: SFElibxmlpp-devel
BuildRequires: SFEnet6-devel
BuildRequires: SFEavahi-devel

%prep
%setup -q -n gobby-%tarball_version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
export CXXFLAGS="%{gcc_cxx_optflags}"
%else
export CXX="${CXX} -norunpath"
export CXXFLAGS="%cxx_optflags"
%endif
export LDFLAGS="%{_ldflags}"

autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-gnome

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
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
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Initial version
