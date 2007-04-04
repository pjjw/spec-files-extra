#
# spec file for package SFElibmpcdec
#
# includes module(s): libmpcdec
#
%include Solaris.inc

Name:                    SFElibmpcdec
Summary:                 libmpcdec - Portable Musepack decoder library
Version:                 1.2.5
Source:                  http://files2.musepack.net/source/libmpcdec-%{version}.tar.bz2
Patch1:			 libmpcdec-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: SFElibsndfile
BuildRequires: SFElibsndfile-devel
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmpcdec-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPPFLAGS="-D__inline=inline"
export CFLAGS="%optflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Apr 05 2007 - Thomas Wagner
- bump to 1.2.5
- refresh patch/libmpcdec-01-configure.diff
* Fri Jun 23 2006 - laca@sun.com
- rename to SFElibmpcdec
- update file attributes
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Initial version
