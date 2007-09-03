#
# spec file for package SFEgtk-sharp
#
# includes module(s): gtk-sharp
#
%include Solaris.inc

Name:         SFEgtk-sharp
License:      Other
Group:        System/Libraries
Version:      2.10.2
Summary:      gtk# - .NET bindings for the gtk+
Source:       http://go-mono.com/sources/gtk-sharp-2.10/gtk-sharp-%{version}.tar.bz2
Patch1:       gtk-sharp-01-fix-prototype.diff
%define gtk_sharp_1_version 1.0.10
Source1:      http://go-mono.com/sources/gtk-sharp/gtk-sharp-%{gtk_sharp_1_version}.tar.gz
URL:          http://www.mono-project.com/Gtk
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SUNWgnome-base-libs
BuildRequires: SFEmono-devel
BuildRequires: SFEmonodoc
Requires: SUNWgnome-base-libs
Requires: SFEmono

%prep
%setup -q -c -n %name-%version
gzip -dc %SOURCE1 | tar xf -

cd gtk-sharp-%{gtk_sharp_1_version}
%patch1 -p1
cd ..

cd gtk-sharp-%{version}
%patch1 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

cd gtk-sharp-%{gtk_sharp_1_version}
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS CFLAGS="$CFLAGS"
cd ..

cd gtk-sharp-%{version}
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS CFLAGS="$CFLAGS"

%install
cd gtk-sharp-%{gtk_sharp_1_version}
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

cd gtk-sharp-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %dir %{_libdir}/gtk-sharp-2.0
%{_libdir}/gtk-sharp-2.0/*
%dir %attr (0755, root, bin) %dir %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, bin) %dir %{_libdir}/monodoc
%{_libdir}/monodoc/*
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gapi-2.0
%{_datadir}/gapi

%changelog
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Bump to 2.10.2
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 2.8.3
* Sun Jul 23 2006 - laca@sun.com
- rename to SFEgtk-sharp
- update CFLAGS/LDFLAGS
- add gtk-sharp-1
* Wed Jul 13 2006 - jedy.wang@sun.com
- Initial spec
