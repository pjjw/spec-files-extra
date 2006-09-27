#
# spec file for package SFElibcm
#
# includes module(s): libcm
#
# Note that the Composite Manager library is experimental code for 
# turning on compositing in metacity.  You probably need Xorg 7.1
# to build with this, and the Xcomposite extension isn't yet in
# Solaris Nevada by default, so you need to build Xorg 7.1 to
# build/test this code.
#
# After building this code, you need to rebuild SUNWgnome-wm using
# the jds-spec-files and CBE.  Note you need to add
# --enable-compositor to the metacity.spec file call to configure.
# Also note that after rebuilding, you need to turn on GConf setting
# apps->metacity->general->compositing_manager to turn the feature on.
# This doesn't really seem to work very well for me, and just crashes,
# though I didn't do a full 7.1 Xorg rebuild so that may be my 
# problem.  Making this available if others want to build and test
# this code out.
#
%include Solaris.inc

Name:                    SFElibcm
Summary:                 Composite Manager library for Metacity
Version:                 0.0.22
Source:                  http://ftp.gnome.org/pub/GNOME/sources/libcm/2.16/libcm-%{version}.tar.bz2
Patch1:                  libcm-01-fixcompile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n libcm-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/openwin/lib -R/usr/openwin/lib -L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib -lX11 -lXcomposite -lXtst -lXdamage -lXfixes"
export MSGFMT="/usr/bin/msgfmt"

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Sep 27 2006 - brian.cameron@sun.com
- created.
