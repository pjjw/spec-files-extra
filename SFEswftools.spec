#
# spec file for package SFEswftools
#
# includes module(s): swftools
#

%include Solaris.inc

%define src_name     swftools
%define src_url      http://www.swftools.org

Name:                SFEswftools
Summary:             SWF manipulation and generation utilities
Version:             0.8.1
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:              swftools-01-sunpro.diff
Patch2:              swftools-02-destdir.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWjpg
Requires: SUNWfreetype2
Requires: SUNWlibC
#Requires: SFElame
#BuildRequires: SFElame-devel
Requires: SFEgiflib
BuildRequires: SFEgiflib-devel

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --disable-lame

make -j$CPUS

%install
rm -rf "$RPM_BUILD_ROOT"
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/swftools
%{_datadir}/swftools/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sat Jun 07 2008 - trisk@acm.jhu.edu
- Initial spec
