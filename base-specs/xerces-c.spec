Name:         xerces-c
Group:        System/Libraries
Version:      2.8.0
%define tarball_version 2_8_0
Summary:      Xerces-C++ - validating XML parser
Source:       http://www.apache.org/dist/xerces/c/sources/xerces-c-src_%{tarball_version}.tar.gz
URL:          http://xerces.apache.org/index.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n xerces-c-src_%{tarball_version}

%build
# don't try to parallel build this
CPUS=1

export XERCESCROOT=`pwd`
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%_ldflags %{cxx_optflags}"
cd $XERCESCROOT/src/xercesc
./runConfigure %{rcopts} -c `basename ${CC}` -x `basename ${CXX}` -p solaris -C \
    --libdir="%{_libdir}" -minmem -nsocket -tnative -r pthread \
    -P%{_prefix}
make -j $CPUS DESTDIR=$RPM_BUILD_ROOT

%if %{?no_samples:%no_samples}%{!?no_samples:0}
%else
cd $XERCESCROOT/samples
./runConfigure %{rcopts} -c ${CC} -x "${CXX}" -p solaris -r pthread
make -j $CPUS DESTDIR=$RPM_BUILD_ROOT
%endif

%install
export XERCESCROOT=`pwd`
cd $XERCESCROOT/src/xercesc
make DESTDIR=$RPM_BUILD_ROOT TARGET=$RPM_BUILD_ROOT install

%if %{?no_samples:%no_samples}%{!?no_samples:0}
%else
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
#we don't want obj directory
install `/usr/gnu/bin/find $XERCESCROOT/bin -maxdepth 1 -type f` \
    $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xerces-c
/usr/gnu/bin/cp -a $XERCESCROOT/samples $RPM_BUILD_ROOT%{_datadir}/xerces-c
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755, root, bin)
%{_bindir}/*
%{_libdir}/libxerces-*.so.*
%{_libdir}/libxerces-*.so

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xerces-c/samples

%changelog
* Sun Feb 17 2008 - laca@sun.com
- create based on xerces-c.spec distributed with Xerces-C-2.8.0
