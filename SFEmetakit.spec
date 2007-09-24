#
# spec file for package SFEmetakit.spec
#
# includes module(s): metakit
#
%include Solaris.inc

%define python_version 2.4
%define tcl_version 8.4
%define tcl_8_3 %(pkgchk -l SUNWTcl 2>/dev/null | grep /usr/sfw/bin/tclsh8.3 >/dev/null && echo 1 || echo 0)

%define src_name	metakit
%define src_url		http://www.equi4.com/pub/mk/

Name:                   SFEmetakit
Summary:                Metakit - Efficient embedded database library
URL:                    http://www.equi4.com/metakit/
Version:                2.4.9.7
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:                 metakit-01-sunpro.diff
Patch2:                 metakit-02-wideint.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
BuildRequires: SUNWPython-devel
BuildRequires: SUNWPython
BuildRequires: SUNWTcl
%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%package python
Summary:                 Mk4py - Python bindings for Metakit
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWPython

%package tcl
Summary:                 Mk4tcl - Tcl bindings for Metakit
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWTcl

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd unix
libtoolize --force --copy
aclocal
autoheader
autoconf --force
cd ..

cd builds
export CXX="${CXX} -norunpath"
export CXXFLAGS="%cxx_optflags -mt -I/usr/sfw/include"
%if %tcl_8_3
export LDFLAGS="%_ldflags -mt -L/usr/sfw/lib -R/usr/sfw/lib"
TCL_OPTS="--with-tcl=/usr/sfw/include,/usr/sfw/lib/tcl8.3"
%else
export LDFLAGS="%_ldflags -mt"
TCL_OPTS="--with-tcl=%{_includedir},%{_libdir}/tcl%{tcl_version}"
%endif
../unix/configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --enable-threads		\
            --enable-shared		\
	    --disable-static		\
            $TCL_OPTS			\
            --with-python=%{_includedir}/python%{python_version},%{_libdir}/python%{python_version}/vendor-packages

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd builds
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%files python
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python*

%files tcl
%defattr (-, root, bin)
%if %tcl_8_3
%dir %attr (0755, root, bin) %{_prefix}/sfw
%dir %attr (0755, root, bin) %{_prefix}/sfw/lib
%{_prefix}/sfw/lib/tcl*
%else
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tcl*
%endif

%changelog
* Mon Sep 24 2007 - trisk@acm.jhu.edu
- Initial spec
