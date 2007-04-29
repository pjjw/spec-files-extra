#
# spec file for package SFEfreetype
#
# includes module(s): GNU freetype
#
%include Solaris.inc
%include usr-gnu.inc

%define src_name     freetype
Name:                SFEfreetype
Summary:             Freetype
Version:             2.3.4
Source:              http://savannah.nongnu.org/download/%{src_name}/%{src_name}-%{version}.tar.bz2
Patch1:		     freetype-01-options.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"


bash ./autogen.sh
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --includedir=%{_includedir}		\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial spec - some apps need modern freetype
