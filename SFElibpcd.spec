#
# spec file for package SFElibpcd
#
# includes module(s): libpcd
#
%include Solaris.inc

%define	src_name libpcd
%define	src_url http://dl.bytesex.org/releases/libpcd

Name:                SFElibpcd
Summary:             Library for reading PhotoCD images
Version:             1.0.1
Source:              %{src_url}/%{src_name}_%{version}.tar.gz
Patch1:		     libpcd-01-makefile.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export PICFLAGS="-KPIC"
export SHAREDFLAGS="-G -Wl,-h"
export WARN=""
export PREFIX=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon Jul 30 2007 - dougs@truemail.co.th
- Initial spec
