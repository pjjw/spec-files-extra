#
# spec file for package SUNWlcms
#
# temp spec for lcms until SFW integrate it
#



Name:                    SUNWlcms
Summary:                 Little ColorManagement System
Version:                 1.17
Source:                  http://www.littlecms.com/lcms-%{version}.tar.gz
Patch1:                  lcms-01-python-libs.diff
URL:                     http://www.littlecms.com
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: SUNWTiff
Requires: SUNWjpg
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWPython
Requires: SUNWlibC
BuildRequires: SUNWPython-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWzlib
##FIXME## for spec-files-other: shouldn't depend on SFEswig
BuildRequires: SFEswig
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n lcms-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"



export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
aclocal $ACLOCAL_FLAGS
automake -c -f

##FIXME## the solaris bin/amd64/python2.4 has no lib/amd64 counterpart,
##FIXME## this lcms configure script doesn't work with 
##FIXME## PYTHON=/usr/bin/amd64/python2.4 to print out lib/amd64 path for binary python object _lcms.so
##FIXME## /usr/bin/amd64/python2.4  -c "from distutils import sysconfig; print sysconfig.get_python_lib(1,0,prefix='/usr')"

%if %{opt_arch64}
echo "build %{bld_arch} WITHOUT python lib"
export PYTHON=/usr/bin/amd64/python2.4
%elseif
#note: python binary for i386 is not isaexec equipped
echo "build %{bld_arch} WITH python lib"
export PYTHON=/usr/bin/python2.4
%endif

./configure --prefix=%{_prefix} --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
%if %{opt_arch64}
                          \
%elseif
            --with-python \
%endif
            --mandir=%{_mandir} \
            --enable-static=no


make -j$CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

#we have no python2.4 64-bit libraries
%if %{opt_arch64}
%elseif
 cd $RPM_BUILD_ROOT%{_libdir}/python%{python_version}
 mv site-packages vendor-packages
 rm vendor-packages/_lcms.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
#see top level spec

%files devel
#see top level spec

%changelog
* Sat Mar 22 2008 - Thomas Wagner
- temporarily copied SUNWlcms to spec-files-extra from spec-files-other
  to make a 64-bit version. Some time after integration into
  regular builds, this spec will go away from spec-files-extra (avoid duplication)
- build python lib only in 32-bit build, since python2.4 in 64-bit seems to be incomplete
* Sun Sep 16 2007 - dougs@truemail.co.th
- Bump to 1.17
* Tue Feb  6 2007 - damien.carbery@sun.com
- Bump to 1.16. Add aclocal call because automake version mismatch.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFElcms
- update file attributes to match JDS
* Tue Mar 21 2006 - damien.carbery@sun.com
- Minor mods to %files (/usr/lib -> %{_libdir}).
* Fri Mar 17 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
