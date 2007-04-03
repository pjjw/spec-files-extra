# 
# 
# 
%include Solaris.inc

Name:                SFEpine
Summary:             University of Washington Pine mail user agent
Version:             4.64
Source:              ftp://ftp.cac.washington.edu/pine/pine%{version}.tar.gz
URL:                 http://www.washington.edu/pine
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n pine%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./build LOCALPINECFLAGS='-DSYSTEM_PINERC=\"/etc/pine.conf\" -DSYSTEM_PINERC_FIXED=\"/etc/pine.conf.fixed\"' \
        SSLCERTS=/etc/sfw/openssl/certs \
        SSLINCLUDE=/usr/sfw/include \
        SSLLIB=/usr/sfw/lib \
        SSLDIR=/etc/sfw/openssl \
        EXTRALDFLAGS="-R/usr/sfw/lib" \
        DEBUG=-O \
        soc

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -D bin/pine $RPM_BUILD_ROOT%{_bindir}/pine
install -D bin/pico $RPM_BUILD_ROOT%{_bindir}/pico
install -D bin/pilot $RPM_BUILD_ROOT%{_bindir}/pilot
install -D bin/rpload $RPM_BUILD_ROOT%{_bindir}/rpload
install -D bin/rpdump $RPM_BUILD_ROOT%{_bindir}/rpdump
install -D bin/mailutil $RPM_BUILD_ROOT%{_bindir}/mailutil
#
install -D doc/pine.1 $RPM_BUILD_ROOT%{_mandir}/man1/pine.1
install -D doc/pico.1 $RPM_BUILD_ROOT%{_mandir}/man1/pico.1
install -D doc/pilot.1 $RPM_BUILD_ROOT%{_mandir}/man1/pilot.1
install -D doc/rpload.1 $RPM_BUILD_ROOT%{_mandir}/man1/rpload.1
install -D doc/rpdump.1 $RPM_BUILD_ROOT%{_mandir}/man1/rpdump.1
install -D imap/src/mailutil/mailutil.1 $RPM_BUILD_ROOT%{_mandir}/man1/mailutil.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
*
* Tue Apr 03 2007 - Eric Boutilier
- Initial spec
