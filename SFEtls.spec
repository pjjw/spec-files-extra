#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define major_version 1.5
%define minor_version 0

Name:                SFEtls
Summary:             Tcl - Tool Command Language
Version:             %{major_version}.%{minor_version}
Source:              http://dfn.dl.sourceforge.net/sourceforge/tls/tls1.5.0-src.tar.gz
Patch1:              tls-01-destdir.diff
URL:                 http://tls.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWTcl
Requires: SUNWTcl

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n tls%{major_version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export CFLAGS="%optflags"
#export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	    --enable-shared \
	    --with-ssl-dir=/usr/sfw \
	    --enable-threads

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rmdir $RPM_BUILD_ROOT%{_bindir}
#rmdir $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Nov 21 2007 - daymobrew@users.sourceforge.net
- Initial spec
