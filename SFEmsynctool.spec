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
Version:            %{msynctool.version}
SUNW_BaseDir:       /
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWsqlite3
Requires: SUNWlxml
Requires: SUNWmlib
Requires: SUNWzlib
Requires: SFElibopensync
BuildRequires: SUNWcmake
BuildRequires: SUNWsqlite3
BuildRequires: SUNWgnome-base-libs-devel 
BuildRequires: SFElibopensync-devel 

%prep
rm -rf %name-%version
mkdir -p %name-%version
%msynctool.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%msynctool.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%msynctool.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/bash_completion.d


%changelog
* Thu Jan 08 2009 - halton.huo@sun.com
- Use SUNWcmake
- Add /etc/bash_completion.d to %files
- Remove unused %post and %postun
* Thu Sep 04 2008 - halton.huo@sun.com
- Use SFEcmake if cmake is not in $PATH
* Thu Dec 20 2007 - jijun.yu@sun.com
- Delete the build requires SFEscons
- Add the build requires SFEcmake
* Wed Jun 06 2007 - nonsea@users.sourceforge.net
- Add BuildRequires SFEscons and SFEcheck
* Tue Jun 05 2007 - jijun.yu@sun.com
- Splitted from SFEmultisync.spec and bumpped to 0.30
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
