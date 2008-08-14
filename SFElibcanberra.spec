#
# spec file for package SFElibcanberra
#
# includes module(s): libcanberra
#
%include Solaris.inc

Name:                    SFElibcanberra
Summary:                 Event Sound API Using XDG Sound Theming Specification
Version:                 0.6
Source:                  http://www.0pointer.de/public/libcanberra-%{version}.tar.gz
Patch1:                  libcanberra-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libcanberra-%version
%patch1 -p1 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

glib-gettextize -f
libtoolize --copy --force
#
# Adding /opt/dtbld/share/aclocal to ACLOCAL_FLAGS is bad, but it works until
# the CBE is fixed.
#
aclocal $ACLOCAL_FLAGS -I /opt/dtbld/share/aclocal
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

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
%{_libdir}/gtk-2.0
%{_libdir}/libcanberra
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%{_datadir}/gtk-doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Aug 14 2008 - brian.cameron@sun.com
- Created with version 0.6.
