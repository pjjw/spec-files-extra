#
# spec file for package SFEdovecot
#

##TODO## create SMF manifest to autostart dovecot
##TODO## check if adding pam settings is necessary (by one-time SMF service)
##TODO## add convenient helper for generating a default configuration file, by default with SSL enabled
##TODO## add convenient helper for generating SSL-certificates, make one-time SMF service calling that helper on request

%define src_name dovecot
# maybe set to nullstring outside release-candidates (example: 1.1/rc)
%define downloadversion	 1.1/rc

%include Solaris.inc
Name:                    SFEdovecot
Summary:                 dovecot - A Maildir based pop3/imap email daemon
URL:                     http://www.dovecot.org
#note: see downloadversion above
Version:                 1.1.rc5
Source:                  http://dovecot.org/releases/%{downloadversion}/%{src_name}-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWzlib
BuildRequires: SUNWopenssl-includes
Requires: SUNWzlib
Requires: SUNWopenssl-libraries

%include default-depend.inc

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /


%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#lib|libexec tweaked bcs. names used twice as files and directories ... "imap" and "pop3"
#/usr/libexec
#/usr/libexec/dovecot
#/usr/lib
#/usr/lib/dovecot
#/usr/lib/dovecot/auth
#/usr/lib/dovecot/imap
#/usr/lib/dovecot/lda
#/usr/lib/dovecot/pop3

# we want:
#/usr/lib/dovecot/bin
#/usr/lib/dovecot/auth
#/usr/lib/dovecot/imap
#/usr/lib/dovecot/lda
#/usr/lib/dovecot/pop3


./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}/%{src_name} \
            --datadir=%{_datadir}	\
            --libexecdir=%{_libdir}/%{src_name}/bin \
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --enable-shared		\
	    --disable-static		


gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/include


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755,root,bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/%{src_name}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*



%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*


%changelog
* Thu May 22 2008  - Thomas Wagner
- Initial spec
