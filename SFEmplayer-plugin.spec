#
# spec file for package SFEmplayer-plugin.spec
#
# includes module(s): mplayerplug-in
#
%include Solaris.inc

Name:                    SFEmplayer-plugin
Summary:                 mplayerplug-in - MPlayer plugin for firefox
Version:                 3.25
Source:                  http://easynews.dl.sourceforge.net/sourceforge/mplayerplug-in/mplayerplug-in-%{version}.tar.gz
Patch1:			 mplayerplugin-01-makefile.diff
Patch2:                  mplayerplugin-02-strings_h.diff
Patch3:                  mplayerplugin-03-strstr.diff
Patch4:                  mplayerplugin-04-ndelay.diff
Patch5:                  mplayerplugin-05-install.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWfirefox
BuildRequires: SUNWfirefox-devel
Requires: SFEmplayer

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n mplayerplug-in
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%ifarch sparc
export CFLAGS="-xO5 -xlibmil -DG_GNUC_INTERNAL=\"\""
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife -DG_GNUC_INTERNAL=\"\""
%else
export CFLAGS="-xO3 -xlibmil -DG_GNUC_INTERNAL=\"\""
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife -DG_GNUC_INTERNAL=\"\""
%endif

CPPFLAGS="-I/usr/include/firefox"                   \
LDFLAGS="-L/usr/lib/firefox -R/usr/lib/firefox"    \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
	    --enable-rpath --enable-wmp      \
            --enable-qt                      \
            --disable-rm                     \
            --enable-gmp

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
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Jun 30 2006 - laca@sun.com
- rename to SFEmplayer-plugin
- define l10n pkg
- update file attributes
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
