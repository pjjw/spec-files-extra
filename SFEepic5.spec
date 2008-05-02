#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEepic5
Summary:             Scriptable, text-based ircII-derived IRC client (development version)
Version:             0.3.8
Source:              ftp://ftp.epicsol.org/pub/epic/EPIC5-ALPHA/epic5-0.3.8.tar.gz
Patch1:              epic5-01-void-return.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n epic5-%version
%patch1 -p0

%build

export CFLAGS="%optflags -I/usr/sfw/include -xO3"
export LDFLAGS="%{_ldflags} -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libdir}/epic5 \
            --with-ipv6 \
            --with-ssl=/usr/sfw \
            --with-iconv \
            --with-perl \
            --with-tcl=/usr/lib/tclConfig.sh \
            --with-ruby

make

%install
rm -rf $RPM_BUILD_ROOT

make install IP=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/epic5
%{_libdir}/epic5/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/epic5
%dir %attr (0755, root, sys) %{_datadir}/epic5/script
%{_datadir}/epic5/script/*
%dir %attr (0755, root, sys) %{_datadir}/epic5/help
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1

%changelog
* Tue May  2 2008 - river@wikimedia.org
- Initial spec
