#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEjasper
License:             Jasper Software License
Summary:             A free software-based reference implementation of the JPEG-2000 Part-1 CODEC
Version:             1.900.1
URL:                 http://www.ece.uvic.ca/~mdadams/jasper/
Source:              http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
Source1:             http://www.ece.uvic.ca/~mdadams/jasper/LICENSE

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n jasper-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
gnu_prefix=`dirname %{gnu_bin}`

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no  \
            --with-pic          \
            --without-docs

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/jasper
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/doc/jasper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Initial spec.
