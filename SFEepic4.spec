#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEepic4
Summary:             Scriptable, text-based ircII-derived IRC client (stable version)
Version:             2.10
Source:              ftp://ftp.epicsol.org/pub/epic/EPIC4-PRODUCTION/epic4-2.10.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n epic4-%version

%build

export CFLAGS="%optflags -I/usr/sfw/include -xO3"
export LDFLAGS="%{_ldflags} -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libdir}/epic4 \
            --with-ipv6 \
            --with-ssl=/usr/sfw \
            --with-perl=/usr/perl5/5.8.4/lib/i86pc-solaris-64int/CORE

make

%install
rm -rf $RPM_BUILD_ROOT

make install IP=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/epic4
%{_libdir}/epic4/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/epic
%dir %attr (0755, root, sys) %{_datadir}/epic/script
%{_datadir}/epic/script/*
%dir %attr (0755, root, sys) %{_datadir}/epic/help
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1

%changelog
* Tue May  2 2008 - river@wikimedia.org
- Initial spec
