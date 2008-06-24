#
# spec file for package SFEslib
#
# includes module(s): slib
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc
%define guile_maj_ver    1.8
%use slib = slib.spec

Name:               SFEslib
Summary:            slib - platform independent library for scheme
Version:            %{slib.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEguile-devel
Requires: SFEguile


%prep
rm -rf %name-%version
mkdir -p %name-%version
%slib.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%slib.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%slib.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -L /usr/share/guile/%{guile_maj_ver}/slib ]; then
  rm /usr/share/guile/%{guile_maj_ver}/slib
fi
ln -s %{_datadir}/slib /usr/share/guile/%{guile_maj_ver}/slib

# Rebuild catalogs for as many implementations as possible.
cd %{_datadir}/slib/
make catalogs

%preun
if [ -L /usr/share/guile/%{guile_maj_ver}/slib ]; then
  rm /usr/share/guile/%{guile_maj_ver}/slib
fi
if  [ -f /usr/share/guile/site/slibcat ]; then
  rm /usr/share/guile/site/slibcat
fi

cd %{_datadir}/slib/
rm -f slib.image

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/slib
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/slib
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Split into base/slib.spec
- Add %post and %preun
* Mon Mar 10 2008 - nonsea@users.sourceforge.net
- sed has no option '-s', fix this buidl error
- use man1dir instead of mandir
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 3b1
* Fri Nov 23 2007 - daymobrew@users.sourceforge.net
- Install .scm files under guile directory:
  %{_datadir}/guile/%{guile_maj_version}/slib
- Add Build/Requires SFEguile/-devel.
* Fri Nov 23 2007 - daymobrew@users.sourceforge.net
- Initial spec.
