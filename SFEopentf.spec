#
# spec file for package SFEopentf
#
# includes module(s): opentf
#
%include Solaris.inc

Name:         SFEopentf
License:      BSD
Group:        Applications
Version:      0.6.0
Summary:      Client and associated assemblies for Team Foundation
Source:       http://opentf.googlecode.com/files/opentf-%version.tgz
URL:          http://code.google.com/opentf/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SUNWgnome-base-libs
BuildRequires: SFEmono-devel
BuildRequires: SFEasciidoc
BuildRequires: SFExmlto
Requires: SFEmono

%prep
%setup -q -n opentf-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make # -j $CPUS
perl -pi -e 's,/usr/bin/mono,%{_prefix}/mono/bin/mono,g' tools/opentf/*.sh

%install
export PATH=/usr/mono/bin:$PATH
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/mono
%{_libdir}/opentf
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Mon Apr 28 2008 - trisk@acm.jhu.edu
- Initial spec
