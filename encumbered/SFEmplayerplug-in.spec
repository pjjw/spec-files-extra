#
# spec file for package SFEmplayerplug-in.spec
#
#
%include Solaris.inc

Name:                    SFEmplayerplug-in
Summary:                 MPlayer plugin for Firefox
Version:                 3.55
Source:                  %{sf_download}/mplayerplug-in/mplayerplug-in-%{version}.tar.gz
Patch1:			 mpplugin-01-makefile.diff
Patch2:                  mpplugin-02-strings_h.diff
Patch3:                  mpplugin-03-strstr.diff
Patch4:                  mpplugin-04-ndelay.diff
Patch5:                  mpplugin-05-install.diff
URL:                     http://mplayerplug-in.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWfirefox
BuildRequires: SUNWfirefox-devel
Requires: SFEmplayer
Requires: %name-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n mplayerplug-in-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="%gcc_optflags" 
export LDFLAGS="%_ldflags -L/usr/lib/firefox -R/usr/lib/firefox"
export CXXFLAGS="%gcc_cxx_optflags"
export CPPFLAGS="-I/usr/include/firefox"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
	    --enable-rpath --enable-wmp      \
            --enable-qt                      \
            --disable-rm                     \
            --enable-gmp                     \


make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_libdir}
mv mozilla firefox

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rmdir $RPM_BUILD_ROOT%{_datadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin) 
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files root
%defattr (-, root, sys) 
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Oct 31 2008 - Andras Barna (andras.barna@gmail.com)
- restore, cleanup
* Sat Sep 29 2007 - dick@nagual.nl
- Bumped to the latest stable release v2.45
* Sun May 20 2007 - dick@nagual.nl
- Changed the code patchfiles to apply to the latest code
  As of this writing version 3.40 (and higher)
* Fri Jan  5 2007 - laca@sun.com
- add -I/usr/include/mps to CFLAGS because some headers are no longer
  delivered in SUNWfirefox in favour of mps
* Wed Oct 11 2006 - laca@sun.com
- bump to 3.31
* Fri Jun 30 2006 - laca@sun.com
- rename to SFEmplayer-plugin
- define l10n pkg
- update file attributes
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
