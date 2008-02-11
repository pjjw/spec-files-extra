#
# spec file for package SFEcdcollect
#
# includes module(s): cdcollect
#
%include Solaris.inc

Name:         SFEcdcollect
Version:      0.6.0
Summary:      CDCollect -  a CD catalog application for gnome.
Source:       %{sf_download}/cdcollect/cdcollect-%{version}.tar.bz2
URL:          http://cdcollect.sourceforge.net/index.php
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SFEmono-devel
BuildRequires: SFEgtk-sharp
BuildRequires: SUNWsqlite-devel
Requires: SFEmono
Requires: SFEgtk-sharp
Requires: SUNWsqlite

%package root
Summary:                 %{summary} - / filesystem
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n cdcollect-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --disable-scrollkeeper \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

perl -pi -e 's/^mono /exec \/usr\/mono\/bin\/mono /' \
    $RPM_BUILD_ROOT%{_bindir}/cdcollect
perl -pi -e 's/^#!\/bin\/sh/#!\/bin\/bash/' $RPM_BUILD_ROOT%{_bindir}/cdcollect

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/gtk-update-icon-cache || exit 0';
  echo '/usr/bin/gtk-update-icon-cache --force %{_datadir}/icons/hicolor'
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -t 5
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
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/cdcollect
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%files root
%defattr (0755, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Sep 07 2007 - flistellox@gmail.com
- Initial spec
