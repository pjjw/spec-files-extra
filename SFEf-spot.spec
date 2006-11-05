#
# spec file for package SFEf-spot
#
# includes module(s): f-spot
#
%include Solaris.inc

Name:         SFEf-spot
Version:      0.2.2
Summary:      f-spot - personal photo management application for the GNOME Desktop
Source:       http://ftp.gnome.org/pub/GNOME/sources/f-spot/0.2/f-spot-%{version}.tar.bz2
URL:          http://f-spot.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEmono-devel
BuildRequires: SFElcms-devel
Requires: SUNWgnome-base-libs
Requires: SFEmono
Requires: SFElcms

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd f-spot-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

cd f-spot-%{version}

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --without-gnome-screensaver \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd f-spot-%{version}
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/f-spot/lib*a

perl -pi -e 's/^exec (.*) mono /exec $1 \/usr\/mono\/bin\/mono /' \
    $RPM_BUILD_ROOT%{_bindir}/f-spot
perl -pi -e 's/^#!\/bin\/sh/#!\/bin\/bash/' $RPM_BUILD_ROOT%{_bindir}/f-spot

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/f-spot
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Oct 15 2006 - laca@sun.com
- add pkgconfig .pc file to %files
* Sat Oct 14 2006 - laca@sun.com
- bump to 0.2.2; delete upstream patch solaris.diff
* Wed Oct 11 2006 - laca@sun.com
- add lcms dependency
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 0.2.0
* Mon Jul 24 2006 - laca@sun.com
- create!
