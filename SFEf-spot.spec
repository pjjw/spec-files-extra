#
# spec file for package SFEf-spot
#
# includes module(s): f-spot
#
%include Solaris.inc

Name:         SFEf-spot
Version:      0.1.11
Summary:      f-spot - personal photo management application for the GNOME Desktop
Source:       http://ftp.gnome.org/Public/GNOME/sources/f-spot/0.1/f-spot-0.1.11.tar.bz2
Patch1:       f-spot-01-prctl.diff
URL:          http://f-spot.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEmono-devel
Requires: SUNWgnome-base-libs
Requires: SFEmono

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
%patch1 -p1 -b .prctl

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
* Mon Jul 24 2006 - laca@sun.com
- create!
