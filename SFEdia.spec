#
# spec file for package SFEdia
#
# includes module(s): dia
#

%include Solaris.inc

Name:                    SFEdia
Summary:                 Dia
Version:                 0.96.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/dia/0.96/dia-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgccruntime
Requires: SUNWgccruntime

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n dia-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags "
export CPPFLAGS="-L/usr/sfw"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags -L/usr/sfw/lib"
export CC="cc %optflags"

libtoolize --copy --force
glib-gettextize -f
intltoolize --force --copy
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

#find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
#find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
#find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'
#find $RPM_BUILD_ROOT -type f -name "*.pyc" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_bindir}/dia
%defattr(-, root, bin)
%{_libdir}/dia
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/man
%dir %attr (0755, root, other) %{_datadir}/mime-info
%dir %attr (0755, root, bin) %{_datadir}/omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%dir %attr (0755, root, other) %{_datadir}/oaf
%{_datadir}/applications/dia.desktop
%{_datadir}/dia
%{_datadir}/doc/*
%{_datadir}/man/*
%{_datadir}/omf/*
%{_datadir}/mime-info/*
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Mon Jun 23 2008 - matt.keenan@sun.com
- Initial spec file
