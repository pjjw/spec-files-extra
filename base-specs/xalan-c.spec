Name:         xalan-c
License:      Other
Group:        System/Libraries
Version:      1.10
%define tarball_version 1_10_0
Summary:      XSLT processor for transforming XML documents into other document types
Source:       http://apache.oregonstate.edu/xml/xalan-c/Xalan-C_%{tarball_version}-src.tar.gz
Patch1:       xalan-c-01-sparcv9.diff
URL:          http://xml.apache.org/xalan-c/index.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
Requires:     xerces-c

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
Requires:      %name

%prep
%setup -q -n xml-xalan
%patch1 -p1

%build
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%_ldflags -L%{_cxx_libdir} -R%{_cxx_libdir} %{cxx_optflags}"

export XERCESCROOT=/usr

cd c
export XALANCROOT=`pwd`

./runConfigure %{rcopts} -c `basename ${CC}` -x `basename ${CXX}` -p solaris \
    -C --prefix="%{_prefix}" -P %{_prefix} -z "${CXXFLAGS}" -l "${LDFLAGS}"

make DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
cd c
export XALANCROOT=`pwd`
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/Xalan

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/xalanc

%changelog
* Sun Feb 17 2008 - laca@sun.com
- create
