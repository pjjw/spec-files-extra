#
# spec file for package SFElibstatgrab.spec
#
# includes module(s): libstatgrab
#
%include Solaris.inc

%define src_name	libstatgrab
%define src_url	    http://ftp.uk.i-scream.org/sites/ftp.i-scream.org/pub/i-scream/libstatgrab
%define src_version	0.15
%define pkg_release	1

SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFElibstatgrab
Summary:                libstatgrab - Cross platform library to access system statistics
Version:                0.15
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms
BuildRequires: SUNWgcc

%prep
%setup -q -n %{src_name}-%{version}
export CC=gcc
export CXX=g++
export CFLAGS="-I /usr/gnu/include"
export LDFLAGS="-R /usr/gnu/lib"
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir} \
            --with-curses-prefix=/usr/gnu
%build
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.so
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%dir %attr(0755,root,bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Oct 17 2007 - laca@sun.com
- fix packaging; delete lib*.la lib*.a
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

