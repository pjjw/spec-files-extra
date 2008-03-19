#
# spec file for package SFExalan-c-gpp
#
# includes module(s): Xalan-C
#

%include Solaris.inc

%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%define arch_ldadd -Wl,-znolazyload -Wl,-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}
%define _libdir %{_cxx_libdir}
%define rcopts -b 64
%use xalan64 = xalan-c.spec
%endif

%include base.inc
%define _libdir %{_cxx_libdir}
%define rcopts -b 32
%use xalan = xalan-c.spec

Name:         SFExalan-c-gpp
License:      Other
Group:        System/Libraries
Version:      %{xalan.version}
Summary:      XSLT processor for transforming XML documents into other document types - g++-build libraries
URL:          http://xml.apache.org/xalan-c/index.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
%include default-depend.inc
Requires:     SFExerces-c
BuildRequires: SUNWgnugetopt

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%xalan64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%xalan.prep -d %name-%version/%{base_arch}

%build
export CC=gcc
export CXX=g++

%ifarch amd64 sparcv9
%xalan64.build -d %name-%version/%_arch64
%endif

%xalan.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%xalan64.install -d %name-%version/%_arch64
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_prefix}/lib/lib* $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
%endif

%xalan.install -d %name-%version/%{base_arch}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_prefix}/lib/lib* $RPM_BUILD_ROOT%{_libdir}

rm -rf $RPM_BUILD_ROOT%{_includedir}

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/libxalan-*.so.*
%{_libdir}/%{_arch64}/libxalan-*.so
%endif

%changelog
* Sun Feb 17 2008 - laca@sun.com
- create
