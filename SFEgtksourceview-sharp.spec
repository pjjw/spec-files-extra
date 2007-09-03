#
# spec file for package SFEgtksourview-sharp
#
# includes module(s): gtksourceview-sharp
#
%include Solaris.inc

Name:         SFEgtksourceview-sharp
License:      Other
Group:        System/Libraries
Version:      0.11
Summary:      gtk# - .NET bindings for libgtksourceview
Source:       http://go-mono.com/sources/gtksourceview-sharp-2.0/gtksourceview-sharp-2.0-%{version}.tar.bz2
URL:          http://www.mono-project.org/
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
%setup -q -n gtksourceview-sharp-2.0-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# conflicts with SUNWgnome-gtksourceview
rm $RPM_BUILD_ROOT%{_datadir}/gtksourceview-1.0/language-specs/nemerle.lang
rm $RPM_BUILD_ROOT%{_datadir}/gtksourceview-1.0/language-specs/vbnet.lang

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, bin) %dir %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, bin) %dir %{_libdir}/monodoc
%{_libdir}/monodoc/*
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gapi-2.0
%{_datadir}/gtksourceview-1.0

%changelog
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Bump to 0.11
* Sat Mar 17 2007 - laca@sun.com
- Initial spec
