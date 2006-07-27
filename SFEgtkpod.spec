#
# spec file for package SFEgtkpod
#
# includes module(s): gtkpod
#

%include Solaris.inc

Name:         SFEgtkpod
Summary:      GtkPod - gtk+ based GUI for Apple's iPod
License:      GPL
Group:        System/GUI/GNOME
Version:      0.99.4
Release:      1
Source:       http://umn.dl.sourceforge.net/sourceforge/gtkpod/gtkpod-%{version}.tar.gz
Patch1:       gtkpod-01-fixcompile.diff
URL:          http://www.gtkpod.org
SUNW_BaseDir: %{_prefix}
BuildRoot:    %{_tmppath}/gtkpod-%{version}-build
%include default-depend.inc
BuildRequires: SFEfaad2-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFElibgpod-devel
BuildRequires: SFElibid3tag-devel
Requires: SUNWgnome-base-libs
Requires: SFEfaad2
Requires: SFElibgpod
Requires: SFElibid3tag
Requires: SUNWbash
Requires: SUNWperl584core

%description
gtkpod is a platform independent Graphical User Interface for Apple's
iPod using GTK2. It supports the first to fifth Generation including
the iPod mini, iPod Photo, iPod Shuffle, iPod nano, and iPod Video.

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gtkpod-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export LDFLAGS="%_ldflags -L/usr/X11/lib -R /usr/X11/lib -lX11"
export CFLAGS="%optflags"

glib-gettextize -f
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir}         \
        --localstatedir=/var/lib    \
        --x-includes=/usr/X11/include  \
        --x-libraries=/usr/X11/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtkpod

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEgtkpod
- delete -share subpkg
- delete lots of unnecessary c&p
- add l10n subpkg
- update file attributes
* Fri May 05 2006 - damien.carbery@sun.com
- Remove unneeded intltoolize call.
* Thu Mar 16 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWlibid3tag/-devel and SUNWgnome-libgpod/-devel.
* Thu Mar 09 2006 - brian.cameron@sun.com
- Created
