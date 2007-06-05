#
# spec file for package SFEmsynctool
#
# includes module(s): msynctool.spec 
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner: JerryYu
#

%include Solaris.inc

%use msynctool = msynctool.spec

Name:               SFEmsynctool
Summary:            OpenSync - msynctool - A data synchronization framework CLI
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SUNWmlib
Requires: SUNWzlib
Requires: SFEsqlite
Requires: SFEswig
Requires: SFElibopensync


%prep
rm -rf %name-%version
mkdir -p %name-%version
%msynctool.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%msynctool.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%msynctool.install -d %name-%version


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


%changelog
* Tue Jun 05 2007 - jijun.yu@sun.com
- Splitted from SFEmultisync.spec and bumpped to 0.30
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
