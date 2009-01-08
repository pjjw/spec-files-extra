#
# spec file for package SFElibopensync-plugin-gcal
#
# includes module(s): libopensync-plugin-gcal
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
#

%include Solaris.inc

%use gcal = libopensync-plugin-gcal.spec

Name:               SFElibopensync-plugin-gcal
Summary:            %gcal.summary
Version:            %{gcal.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SFElibopensync
Requires: SFEpython-httplib
BuildRequires: SUNWcmake
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFElibopensync-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gcal.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="-I%{_includedir} %optflags"
export LDFLAGS="-L%{_libdir} -R%{_libdir}"
export RPM_OPT_FLAGS="$CFLAGS"
%gcal.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gcal.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/opensync*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/opensync*

%changelog
* Thu Jan 08 2009 - halton.huo@sun.com
- Use SUNWcmake
* Wed Jan 30 2007 - jijun.yu@sun.com
- Removed the items not in %files
* Thu Dec 20 2007 - jijun.yu@sun.com
- Change %{_datadir}/opensync to %{_datadir}/opensync-1.0
* Tue Aug 07 2007 - jijun.yu@sun.com
- Splitted from SFElibopensync-plugin.spec.
- initial version created.
