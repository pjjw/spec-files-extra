#
# spec file for package SFEmurrine-engine
#
# includes module(s): murrine-engine
#
%include Solaris.inc

%define src_name    murrine
%define src_url     http://murrine.netsons.org/files

Name:			SFEmurrine-engine
Summary:		A GTK2 engine with a modern glassy look
Version:		0.53.1
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
URL:			http://murrine.netsons.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_prefix}

%include default-depend.inc

Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWlexpt
Requires: SUNWzlib

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
            --libdir=%{_libdir}			\
            --enable-animation          \
            --enable-macmenu            \
            --enable-animationtoleft

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Sun Oct 07 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Spec
