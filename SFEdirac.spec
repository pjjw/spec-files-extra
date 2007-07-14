#
# spec file for package SFEdirac.spec
#
# includes module(s): dirac
#
%include Solaris.inc

%define src_name	dirac
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/dirac

Name:                   SFEdirac
Summary:                Dirac video codec
Version:                0.7.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			dirac-01-mmx.spec
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

libtoolize --force --copy
aclocal 
automake --add-missing
autoconf --force

export MMX="--disable-mmx"

export CXX=/usr/sfw/bin/g++
export CXXOPTFLAGS="-O3 -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    $MMX

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial version
