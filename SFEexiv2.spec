#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include usr-gnu.inc

Name:                SFEexiv2
License:             GPL
Summary:             A C++ library and CLI utility to manage image metadata.
Version:             0.16
URL:                 http://www.exiv2.org/
Source:              http://www.exiv2.org/exiv2-%{version}.tar.gz
Patch1:              exiv2-01-makefile.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n exiv2-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl"

extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no  \
            --enable-final	\
            --with-extra-includes="${extra_inc}"

# Fix makefiles as they assume /bin/sh is bash UGH
for mk in `find . -name Makefile`
do
	[ ! -f ${mk}.orig ] && cp ${mk} ${mk}.orig
	cat $mk | sed 's/SHELL = \/bin\/sh/SHELL = \/bin\/bash/' > ${mk}.new
	mv ${mk}.new ${mk}
done
(cd src; cat %{PATCH1} | gpatch -p0)

gmake

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT
%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.la

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%endif

%changelog
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Initial spec.
