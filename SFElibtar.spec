#
# spec file for package SFElibtar
#
# includes module(s): libtar
#
%include Solaris.inc

%define	src_name libtar
%define	src_url	ftp://ftp.feep.net/pub/software/%{src_name}

Name:                SFElibtar
Summary:             C library for manipulating POSIX tar files
Version:             1.2.11
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     libtar-01-shared.diff
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

libtoolize --copy --force
autoconf -f -I autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_bindir}
%{_mandir}/man3

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial spec
