#
# spec file for package SFEmono-addins
#
# includes module(s): mono-addins
#
%include Solaris.inc

Name:         SFEmono-addins
License:      Other
Group:        System/Libraries
Version:      0.2
Summary:      Mono.Addins - a framework for creating extensible applications and add-ins 
Source:       http://go-mono.com/sources/mono-addins/mono-addins-%{version}.tar.gz
URL:          http://www.mono-project.com/Mono.Addins
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SFEmono-devel
Requires: SFEmono

%prep
%setup -q -n mono-addins-%version

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
make -j $CPUS CFLAGS="$CFLAGS"

%install
make DESTDIR=$RPM_BUILD_ROOT install

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, bin) %dir %{_libdir}/mono-addins
%{_libdir}/mono-addins/*
%dir %attr (0755, root, bin) %dir %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Initial spec
