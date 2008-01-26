#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:                SFEwv2
License:             GPL
Summary:             A library that allows access to Microsoft Word files (series 2)
Version:             0.2.3
URL:                 http://wvware.sourceforge.net/
Source:              http://jaist.dl.sourceforge.net/sourceforge/wvware/wv2-%{version}.tar.bz2
Source1:             http://jaist.dl.sourceforge.net/sourceforge/wvware/word_helper.h.diff
## owner:halton date:2007-09-18 bugid:11195 type:bug
#Patch1:              wv-01-solaris-iconv.diff
## owner:halton date:2007-09-18 bugid:11196 type:bug
#Patch2:              wv-02-w3m-dump.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
Requires:            SUNWlxml
Requires:            SUNWzlib
Requires:            SUNWlibmsr
Requires:            SUNWbzip
Requires:            SUNWcslr
Requires:            SFElibgsf
BuildRequires:       SUNWgnome-base-libs-devel
BuildRequires:       SUNWlxml-devel
BuildRequires:       SFElibgsf-devel
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
Requires: SFEgettext
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n wv2-%version
#%patch1 -p1
#%patch2 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
(cd src; cat %{SOURCE1} | gpatch -p0)
gnu_prefix=`dirname %{gnu_bin}`

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-static=no  \
            --with-pic \
            --with-libiconv=${gnu_bin}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Initial spec.
