#
# spec file for package SFElibgpod
#
# includes module(s): libgpod
#

%include Solaris.inc

Name:         SFElibgpod
Summary:      libgpod - a library for accessing the contents of an iPod
License:      GPL
Group:        System/GUI/GNOME
Version:      0.4.0
Release:      1
Source:       http://kent.dl.sourceforge.net/sourceforge/gtkpod/libgpod-%{version}.tar.gz
#this is a workaround, for people using gcc which doesn't not support 
#visibility attribute. the final solution is to change the G_GNUC_INTERNAL macro
#definition in glib.
Patch1:	      libgpod-01-hidden.diff
URL:          http://www.gtkpod.org
SUNW_BaseDir: %{_prefix}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgccruntime
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgcc

#FIXME: update to use (and depend on) HAL when it's integrated into nevada

%description
libgpod is a shared library to access the contents of an iPod.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n libgpod-%version
%patch1 -p1 -b .patch1

# Note, we have to build this with gcc, because Forte cannot handle
# the flexible arrays used in libcdio.  We should move to using Forte
# if this issue is resolved with the Forte compiler.
#
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags -D__hidden="
export CC=gcc

intltoolize --copy --force
libtoolize --force --copy
aclocal $ACLOCAL_FLAGS -I m4
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
        --localstatedir=/var/lib
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/python*

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgpod*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Dec 06 2006 - irene.huang@sun.com
- Change the compiler to be gcc. Removed the old patches
  libgpod-01-fixwall.diff and libgpod-02-fixcompile.diff
  add patch -01-hidden.diff
* Fri Oct 13 2006 - laca@sun.com
- bump to 0.4.0
* Wed Jul  5 2006 - laca@sun.com
- rename to SFElibgpod
- update attributes
- delete lots of unnecessary env variables
- add l10n pkg
- delete unnecessary deps
* Thu Mar 09 2006 - brian.cameron@sun.com
- Created
