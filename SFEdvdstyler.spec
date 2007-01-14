#
# spec file for package SFEDVDStyler
#
# includes module(s): DVDStyler
#
%include Solaris.inc

Name:                    SFEdvdstyler
Summary:                 a dvd building application
Version:                 1.5.0.7
%define tarball_version  1.5b7
Source:                  http://nchc.dl.sourceforge.net/sourceforge/dvdstyler/DVDStyler-%{tarball_version}.tar.gz
Patch1:                  dvdstyler-01-wxwidgets-2.8.diff
Patch2:			 dvdstyler-02-libs.diff
Patch3:			 dvdstyler-03-array.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{tarball_version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEwxwidgets
Requires: SFEwxSVG
Requires: SFEdvdauthor
Requires: SFEmpgtx
Requires: SFEnetpbm
Requires: SFEmjpegtools

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n DVDStyler-%{tarball_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
%ifarch sparc
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=%all"
%else
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=%all"
%endif

touch NEWS
aclocal
autoconf
automake -a
LDFLAGS="-L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib:/usr/sfw/lib" \
CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include" \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/dvdstyler*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%endif


%changelog
* Tue Nov 28 2006 - laca@sun.com
- make it work with either SFEwxwidgets or SFEwxGTK
- change version to numeric
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
