#
# spec file for package SFEeasytag
#
# includes module(s): SFEeasytag
#
%include Solaris.inc

Name:                    SFEeasytag
Summary:                 EasyTag - Modify ID3 Tags
Version:                 1.99.12
Source:                  http://easynews.dl.sourceforge.net/sourceforge/easytag/easytag-%{version}.tar.bz2
Patch1:                  easytag-01-stdc++.diff
URL:			 http://easytag.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEid3lib
Requires: SUNWgnome-libs
Requires: SUNWzlib
Requires: SUNWogg-vorbis
Requires: SUNWflac
#FIXME: version 1.99.12 doesn't seem to be compatible with
#       faad2 2.0
#Requires: SFEfaad2
BuildRequires: SFEid3lib-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWflac-devel
#FIXME BuildRequires: SFEfaad2-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n easytag-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} -lsocket -lnsl"
glib-gettextize -f
aclocal
libtoolize -f
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} \
	--mandir=%{_mandir} --bindir=%{_bindir}         \
        --libdir=%{_libdir}         \
        --includedir=%{_includedir} \
        --disable-mp4
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

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
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/easytag
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man*
%{_mandir}/man*/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
- Fri Jun 23 2006 - laca@sun.com
- rename to SFEeasytag
- clean up env variables
- add patch stdc++.diff which changes some GNU specific libs to Solaris
  specific ones
- autotoolize
- fix file attributes
- create l10n package
- add missing deps
* Fri May 10 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
