#
# spec file for package SFEfreeimage.spec
#
# includes module(s): freeimage
#
%include Solaris.inc

%define src_name	FreeImage
%define src_url		http://jaist.dl.sourceforge.net/sourceforge/freeimage

Name:                   SFEfreeimage
Summary:                free image library
Version:                393
Source:                 %{src_url}/%{src_name}%{version}.zip
Patch1:			freeimage-01-makefile.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}
%patch1 -p1
find . -type f -exec dos2unix {} {} \;

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CXX=/usr/sfw/bin/g++
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make -f Makefile.solaris

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile.solaris install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
