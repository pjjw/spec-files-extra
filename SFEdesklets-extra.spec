#
# spec file for package SUNWgnome-desklets-extra
#
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#


%include Solaris.inc
%use gdesklets = gdesklets-more.spec

Name:                    SFEdesklets-extra
Summary:                 Unsupported desklets
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Requires: SUNWgnome-desklets
Requires: SUNWgnome-desktop-prefs
Requires: SUNWgnome-libs
Requires: SUNWpostrun
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SUNWgnome-libs-devel

%description

%prep
rm -rf %name-%version
mkdir %name-%version

%build
# we just get the bits tarball from developer
%gdesklets.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gdesklets.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%post
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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gdesklets
%{_datadir}/gdesklets/*

%changelog
* Thu Jan 25 2008 - <chris.wang@sun.com>
- initial creation


