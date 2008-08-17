#
# spec file for package SFEpngcrush
#
# includes module(s): pngcrush
#
%include Solaris.inc

%define src_name        pngcrush

Name:                   pngcrush
SUNW_Pkg:               SFEpngcrush
Summary:                pngcrush - utility for recompressing PNG files
Version:                1.6.7
Source:                 http://%{sf_mirror}/sourceforge/pmt/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:         %{name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWzlib

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
make -j$CPUS CC="$CC" LD="$CC" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 pngcrush $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/pngcrush

%changelog
* Thu Aug 14 2008 - laca@sun.com
- create