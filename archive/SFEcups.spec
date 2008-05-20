#
# spec file for package SFEcups
#
# includes module(s): cups
#
%include Solaris.inc

%define	src_ver 1.3.6
%define	src_name cups
%define	src_url	http://ftp.easysw.com/pub/%{src_name}/%{src_ver}

%define cups_user lp
%define cups_group lp
%define cupsdir	/usr/cups
%define cupsbin	%{cupsdir}/bin
%define cupssbin %{cupsdir}/sbin
%define cupsdata %{cupsdir}/share
%define cupsman %{cupsdir}/man

Name:		SFEcups
Summary:	Common Unix Printing System
Version:	%{src_ver}
License:	GPL/LGPL
URL:            http://www.cups.org/
Source:		%{src_url}/%{src_name}-%{version}-source.tar.bz2
Patch1:		cups-01-gss.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
CUPS provides a portable printing layer for UNIX-based operating
systems. It has been developed by Easy Software Products to promote a
standard printing solution for all UNIX vendors and users. CUPS
provides the System V and Berkeley command-line interfaces. CUPS uses
the Internet Printing Protocol ("IPP") as the basis for managing print
jobs and queues. The Line Printer Daemon ("LPD") Server Message Block
("SMB"), and AppSocket (a.k.a. JetDirect) protocols are also supported
with reduced functionality. CUPS adds network printer browsing and
PostScript Printer Description ("PPD") based printing options to
support real-world printing under UNIX.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"

glib-gettextize --force
libtoolize --force --copy
aclocal 
autoconf -f
./configure --prefix=%{_prefix}				\
	    --bindir=%{cupsbin}				\
	    --sbindir=%{cupssbin}			\
	    --libdir=%{_libdir}				\
	    --mandir=%{_mandir}				\
	    --datadir=%{_datadir}			\
	    --sysconfdir=%{_sysconfdir}			\
	    --localstatedir=%{_localstatedir}		\
	    --enable-openssl				\
	    --enable-gnutls				\
	    --disable-gssapi				\
	    --with-cups-user=%{cups_user}		\
	    --with-cups-group=%{cups_group}		\
	    --localedir=%{_datadir}/locale		\
	    --with-openssl-libs=/usr/sfw/lib		\
	    --with-openssl-includes=/usr/sfw/include	\
	    --disable-static				\
	    --enable-shared

make

%install

rm -rf $RPM_BUILD_ROOT
make install BUILDROOT=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/rc*.d
mkdir -p $RPM_BUILD_ROOT%{cupsdata}
mv $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT%{cupsdata}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
( 
  cd $RPM_BUILD_ROOT%{_bindir}
  ln -s ../cups/bin/cups-config 
  for i in cancel lp lpr lpq lprm lpstat ; do
    ln -s ../cups/bin/${i} ${i}-cups
  done
  cd $RPM_BUILD_ROOT%{_sindir}
  for i in accept lpc lpmove lpadmin lpinfo reject ; do
    ln -s ../cups/sbin/${i} ${i}-cups
  done
  ln -s ../cups/sbin/cupsenable enable-cups
  ln -s ../cups/sbin/cupsdisable disable-cups
)

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{cupsdir}
%{cupsbin}
%{cupssbin}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/cups
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{cupsdata}
%{cupsdata}/man
%{_datadir}/cups
%defattr (-, root, other)
%{_datadir}/applications
%{_datadir}/icons

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/cups
%{_sysconfdir}/init.d
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d/cups.conf
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/spool
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/spool/cups
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/spool/cups/tmp
%dir %attr (0755, root, sys) %{_localstatedir}/run
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/run/cups
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/run/cups/certs
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/log/cups
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/cache
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/cache/cups/rss

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Wed Feb 20 2008 - halton.huo@sun.com
- Bump to 1.3.6, move locale into -l10n pkg.
* Wed Aug 15 2007 - dougs@truemail.co.th
- bump to 1.3.0, added --disable-gssapi
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
