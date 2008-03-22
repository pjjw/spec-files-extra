#
# spec file for package SFEgajim.spec
#
# includes module(s): gajim
#

%include Solaris.inc
Name:                    SFEgajim
Summary:                 Gajim Jabber client
Version:                 0.11.4
Source:                  http://www.gajim.org/downloads/gajim-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch2:                  gajim-02-logger.diff
%include default-depend.inc
Requires:                SUNWPython
Requires:                SUNWsqlite3
Requires:                SUNWpysqlite
BuildRequires:           SUNWPython-devel
BuildRequires:           SUNWsqlite3-devel
BuildRequires:           SUNWpysqlite
BuildRequires:           SFEgtkspell-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gajim-%version
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CPPFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"


./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# REMOVE doc FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gajim/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/gajim/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/gajim*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Mar 23 2008 - nicolas@slubman.info
- Bumped version
* Wed Oct 11 2006 - laca@sun.com
- add gtkspell deps
* Wed Jul 26 2006 - lin.ma@sun.com
- Initial spec file
