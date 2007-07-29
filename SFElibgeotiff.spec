#
# spec file for package SFElibgeotiff
#
# includes module(s): libgeotiff
#
%include Solaris.inc

%define	src_name libgeotiff
%define	src_url	ftp://ftp.remotesensing.org/pub/geotiff/%{src_name}

Name:                SFElibgeotiff
Summary:             library for writing GeoTIFF information tags of tiff files
Version:             1.2.4
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     libgeotiff-01-shared.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEproj-devel
Requires: SFEproj
BuildRequires: SUNWjpg-devel
Requires: SUNWjpg
BuildRequires: SUNWTiff-devel
Requires: SUNWTiff

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
export LD_SHARED="$LD -G"

libtoolize --copy --force
aclocal
autoconf -f
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --with-ld-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/epsg_csv

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
