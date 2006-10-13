#
# spec file for package SFEplanner.spec
#
# includes module(s): planner
#

%include Solaris.inc
Name:                    SFEplanner
Summary:                 Gnome Planner. Project planner likes Gantt. 
Version:                 0.14
Source:                  http://ftp.gnome.org/pub/gnome/sources/planner/0.14/planner-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n planner-%version
pwd
sed -e 's/ -W.*$//g' python/Makefile.am > Makefile.$$
mv Makefile.$$ python/Makefile.am
aclocal --force
automake -acf
autoconf -f

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
%else
%endif
export CFLAGS="%optflags"
#export CPPFLAGS="%cxx_optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
./configure --config-cache \
	--prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}	\
	--enable-python-plugin --disable-update-mimedb
make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la


%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo '/usr/bin/update-mime-database %{_datadir}/mime \';
  echo '/usr/bin/update-desktop-database \';
  echo '    > /var/tmp/planner.load' ) | \
      $BASEDIR/lib/postrun -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libplanner-1.so*
%{_libdir}/planner/*
%{_libdir}/python2.4/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/planner/*
%{_datadir}/icons/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/*
%{_datadir}/applications/*
%{_datadir}/gtk-doc/*
%{_datadir}/gnome/*
%{_datadir}/omf/*
%{_datadir}/doc/*

%files root
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}/locale/share
%attr (-, root, other) %{_datadir}/locale/share
%endif

%changelog
* Wed Oct 12 2006 - lin.ma@sun.com
- Initial spec file
