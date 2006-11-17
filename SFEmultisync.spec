#
# spec file for package SFEmultisync
#
# includes module(s): msynctool.spec multisync-gui.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%use msynctool = msynctool.spec
%use msyncgui = multisync-gui.spec

Name:               SFEmultisync
Summary:            OpenSync - multisync - A data synchronization framework CLI/GUI
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SFEsqlite
Requires:           SFEswig
Requires:           SFElibopensync
BuildRequires:      SFEsqlite-devel
BuildRequires:      SFElibopensync-devel


%prep
rm -rf %name-%version
mkdir -p %name-%version
%msynctool.prep -d %name-%version
%msyncgui.prep -d %name-%version


%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%msynctool.build -d %name-%version
%msyncgui.build -d %name-%version


%install
rm -rf $RPM_BUILD_ROOT
%msynctool.install -d %name-%version
%msyncgui.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT


%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait


%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/multisync-gui
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/*


%changelog
- initial version created