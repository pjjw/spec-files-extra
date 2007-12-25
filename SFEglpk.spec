#
# spec file for package SFEglpk
#
# includes module(s): glpk
#

%include Solaris.inc

%define src_url     http://ftp.gnu.org/pub/gnu/glpk
%define src_name    glpk

Name:                SFEglpk
Summary:             The GNU Linear Programming Kit
Version:             4.24
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
URL:                 http://www.gnu.org/software/glpk
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:           SFEgmp
BuildRequires:      SFEgmp-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-D__sun__"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
            --datadir=%{_datadir}       \
            --mandir=%{_mandir}			\
            --docdir=%{_docdir}		    \
            --enable-shared             \
            --disable-static            \
            --enable-gmp

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Dec 25 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial version
