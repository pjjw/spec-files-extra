#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEgd
Summary:             library for the dynamic creation of images by programmers
Version:             2.0.35
Source:              http://www.libgd.org/releases/gd-%{version}.tar.bz2
Url:	    	     http://www.libgd.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWxwplt
BuildRequires: SUNWpng
BuildRequires: SUNWjpg
Requires: SUNWxwplt
Requires: SUNWpng
Requires: SUNWjpg

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n gd-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libgd.la

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
* Sat Aug 18 2007 - trisk@acm.jhu.edu
- Bump to 2.0.35
*
* Tue Mar 22 2007 - Thomas Wagner
- split into SFEgd SFEgd-devel
*
* Tue Mar 20 2007 - Thomas Wagner
- bump up version to 2.0.34
- new Url / Source
* 
* Fri Sep 29 2006 - Eric Boutilier
- Initial spec
