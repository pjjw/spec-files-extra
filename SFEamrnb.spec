#
# spec file for package SFEamrnb
#
# includes module(s): amrnb
#
%include Solaris.inc

%define	src_ver 6.1.0.4
%define	src_name amrnb
%define	src_url	http://ftp.penguin.cz/pub/users/utx/amr

Name:		SFEamrnb
Summary:	3GPP AMR-NB Floating-point Speech Codec
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Source1:	http://www.3gpp.org/ftp/Specs/archive/26_series/26.104/26104-610.zip
Patch1:		amrnb-01-patch.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
3GPP AMR-NB Floating-point Speech Codec.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
cp %{SOURCE1} .
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal
autoconf -f
automake -a -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug

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

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
