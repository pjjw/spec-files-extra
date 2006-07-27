#
# spec file for package SFEdevhelp.spec
#
# includes module(s): devhelp
#

%include Solaris.inc
Name:                    SFEdevhelp
Summary:                 Devhelp provides word-processor-style highlighting and replacement of misspelled words in a GtkTextView widget.
Version:                 0.11
Source:                  http://ftp.gnome.org/pub/GNOME/sources/devhelp/%{version}/devhelp-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWgnome-base-libs
Requires:                SUNWfirefox
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWfirefox-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

%package devel
Summary:                 Devhelp - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n devhelp-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
%else
%endif
export CFLAGS="-i -xO4 -xspace -mr -I/usr/include/firefox -I/usr/include/mps"
export CPPFLAGS="-i -xO3 -xspace -mr -I/usr/include/firefox -I/usr/include/mps"
export CXXFLAGS="-i -xO3 -xspace -mr -I/usr/include/firefox -I/usr/include/mps"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-gtk-doc
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

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/devhelp.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%preun root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/devhelp.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/devhelp
%{_datadir}/devhelp/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/mime-info/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/devhelp.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed July 27 2006 - lin.ma@sun.com
- Initial spec file
