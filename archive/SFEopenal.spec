#
# spec file for package SFEopenal.spec
#
# includes module(s): openal
#
%include Solaris.inc

%define src_name	openal
%define src_url		http://www.openal.org/openal_webstf/downloads

Name:                   SFEopenal
Summary:                OpenAL is a cross-platform 3D audio API
Version:                0.0.8
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			openal-01-inline.diff
Patch2:			openal-02-nasm.diff
Patch3:			openal-03-packed.diff
SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:		openal_license.txt
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%ifarch i386
BuildRequires: SFEnasm
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


%ifarch i386
export CPPFLAGS="-D_XOPEN_SOURCE=600 -D__i386__"
%else
export CPPFLAGS="-D_XOPEN_SOURCE=600"
%endif
export CFLAGS="%optflags -xc99"
export LDFLAGS="%_ldflags"
./autogen.sh
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make clean
make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr(0755,root,bin) %{_libdir}
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jun  5 2007 - dougs@truemail.co.th
- Added patch for Sun Studio 12 builds - openal-03-packed.diff
* Tue May  1 2007 - dougs@truemail.co.th
- Initial version
