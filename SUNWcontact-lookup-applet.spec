#
# spec file for package SUNWcontact-lookup-applet
#
# includes module(s): contact-lookup-applet
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SUNWcontact-lookup-applet
Summary:                 Contact lookup applet
Version:                 0.16
Source:                  http://burtonini.com/computing/contact-lookup-applet-%{version}.tar.gz
Patch1:                  contact-lookup-applet-01-suncc.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %option_with_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
%setup -q -n contact-lookup-applet-%version
%patch1 -p1 -b .patch01

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags"

glib-gettextize --force
aclocal
libtoolize --copy --force
intltoolize --force --copy --automake
automake -a -f
autoconf -f

./configure --prefix=%{_prefix}  \
            --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%if %option_with_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/lookup-applet

%if %option_with_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri May 30 2008 - Jedy Wang (jedy.wang@sun.com)
- Initial spec

