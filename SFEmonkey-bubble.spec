# NOTE:
#
# You need to patch your Sun Studio compiler to be able to build this
# spec file.  Install 121018-07 or later, or
# apply patches/sun-studio-stlport4-fileno.diff
# to file SUNWspro/prod/include/CC/stlport4/stl/_stdio_file.h
# Here's how you do it:
#    $ su -
#    # cd /path/to/SUNWspro/prod/include/CC/stlport4/stl
#    # gpatch -p1 < /path/to/SFE/patches/sun-studio-stlport4-fileno.diff
#

#
# spec file for package SFEmonkey-bubble
#
# includes module(s): monkey-bubble
#
%include Solaris.inc

Name:                    SFEmonkey-bubble
Summary:                 Monkey Bubble arcade game
Version:                 0.4.0
Source:                  http://home.gna.org/monkeybubble/downloads/monkey-bubble-%{version}.tar.gz
URL:                     http://home.gna.org/monkeybubble/
Patch1:                  monkey-bubble-01-build.diff
Group:			 Game/ArcadeGame
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-media
Requires: SUNWgnome-config
Requires: SUNWlibrsvg
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWlibrsvg

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
%setup -q -n monkey-bubble-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CXXFLAGS="%cxx_optflags -library=stlport4 -staticlib=stlport4"
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/gnu/include -DANSICPP"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
libtoolize --copy --force
aclocal-1.9 $ACLOCAL_FLAGS
intltoolize -c -f --automake
autoconf
automake-1.9 -a -c -f
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}         \
            --disable-scrollkeeper

# FIXME: too lazy to fix all broken l10n omf stuff
make -j$CPUS || make || make || make

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

%post root
%include gconf-install.script

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x $PKG_INSTALL_ROOT/usr/bin/gconftool-2 || {';
  echo '  echo "WARNING: gconftool-2 not found; not uninstalling gconf schemas"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$BASEDIR/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$BASEDIR%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/monkey-bubble.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/monkey-bubble
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*
%{_datadir}/omf/*/*-[a-z]*.omf

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/monkey-bubble.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to search paths; intltoolize
* Sun Oct 14 2007 - laca@sun.com
- bump to 0.4.0
* Tue Jul 25 2006 - laca@sun.com
- rename to SFEmonkey-bubble.spec
- update file attribs
- define l10n pkg
- tidy up, use %post/%preun scripts for gconf schemas install
* Tue Oct 25 2005 - glynn.foster@sun.com
- Initial spec
