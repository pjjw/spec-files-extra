#
# spec file for package SFEmonodoc
#
# includes module(s): monodoc
#
%include Solaris.inc

Name:         SFEmonodoc
License:      Other
Group:        System/Libraries
Version:      1.2.3
Summary:      Mono docs
Source:       http://go-mono.com/sources/monodoc/monodoc-%{version}.zip
URL:          http://www.mono-project.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

BuildRequires: SUNWgnome-base-libs
BuildRequires: SFEmono-devel
Requires: SUNWgnome-base-libs
Requires: SFEmono

%prep
%setup -q -n monodoc-%version

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
make # -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/mono
%{_libdir}/monodoc
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sat Apr 27 2007 - dougs@truemail.co.th
- make -j does not always work
* Sat Mar 17 2007 - laca@sun.com
- Initial spec
