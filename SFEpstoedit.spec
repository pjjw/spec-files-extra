#
# spec file for package SFEpstoedit.spec
#
# includes module(s): pstoedit
#
%include Solaris.inc

%define src_name	pstoedit
%define src_url		http://switch.dl.sourceforge.net/%{src_name}

Name:                   SFEpstoedit
Summary:                translates PS and PDF graphics into other formats
Version:                3.44
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export LIBMAGICK_CFLAGS="-I/usr/include"
export LIBMAGICK_LIBS="-lMagick++ -lm"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lm"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm $RPM_BUILD_ROOT%{_libdir}/pstoedit/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/pstoedit
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/pstoedit

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
