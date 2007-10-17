#
# spec file for package SFEgnome-sharp
#
# includes module(s): gnome-sharp
#
%include Solaris.inc

Name:         SFEgnome-sharp
License:      Other
Group:        System/Libraries
Version:      2.16.0
Summary:      gtk# - .NET bindings for the GNOME platform libraries
Source:       http://go-mono.com/sources/gnome-sharp2/gnome-sharp-%{version}.tar.gz
Patch1:       gnome-sharp-01-Wall.diff
Patch2:       gnome-sharp-02-gtkhtml3.14.diff
URL:          http://www.mono-project.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEmono-devel
Requires: SUNWgnome-base-libs
Requires: SUNWevolution-libs
Requires: SFEmono

%prep
%setup -q -n gnome-sharp-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

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
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gapi-2.0

%changelog
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Add gnome-sharp-02-gtkhtml3.14.diff
* Sat Mar 17 2007 - laca@sun.com
- Initial spec
