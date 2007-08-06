#
# spec file for package SFEx264
#
# includes module(s): x264
#

%include Solaris.inc

%define         snap    20070728
%define         snaph   2245
%define src_name x264-snapshot
%define src_url	 ftp://ftp.videolan.org/pub/videolan/x264/snapshots

Name:                    SFElibx264
Summary:                 H264 encoder library
Version:                 20070728
Source:                  %{src_url}/%{src_name}-%{snap}-%{snaph}.tar.bz2
Patch1:			 libx264-01-gccisms.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
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
%setup -q -n %{src_name}-%{snap}-%{snaph}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
bash ./configure	\
    --prefix=%{_prefix} \
    --enable-mp4-output	\
    --enable-gtk	\
    --enable-pthread	\
    --enable-pic	\
    --enable-shared	\
    $nlsopt

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/x264

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- initial version