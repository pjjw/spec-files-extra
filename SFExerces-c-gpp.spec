#
# spec file for package SFExerces-c
#
# includes module(s): Xerces-C++
#

%include Solaris.inc

# don't build the sample code, it's built in the no-gpp spec file
%define no_samples 1
%define cc_is_gcc 1

%ifarch amd64 sparcv9
%include arch64.inc
%define _libdir %{_cxx_libdir}
%define rcopts -b 64
%use xerces64 = xerces-c.spec
%endif

%include base.inc
%define _libdir %{_cxx_libdir}
%define rcopts -b 32
%use xerces = xerces-c.spec

Name:         SFExerces-c-gpp
License:      Other
Group:        System/Libraries
Version:      %{xerces.version}
Summary:      Xerces-C++ - validating XML parser - g++-built libraries
URL:          http://xerces.apache.org/index.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
%include default-depend.inc
BuildRequires: SFEdoxygen
BuildRequires: SFEfindutils
BuildRequires: SUNWgnu-coreutils

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The parser provides high performance, modularity, and scalability. Source
code, samples and API documentation are provided with the parser. For
portability, care has been taken to make minimal use of templates, no RTTI,
and minimal use of #ifdefs.

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%xerces64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%xerces.prep -d %name-%version/%{base_arch}

%build
export CC=gcc
export CXX=g++

%ifarch amd64 sparcv9
%xerces64.build -d %name-%version/%_arch64
%endif

%xerces.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%xerces64.install -d %name-%version/%_arch64
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_prefix}/lib/lib* $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
%endif

%xerces.install -d %name-%version/%{base_arch}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_prefix}/lib/lib* $RPM_BUILD_ROOT%{_libdir}

rm -rf $RPM_BUILD_ROOT%{_includedir}

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755, root, bin)
%{_libdir}/libxerces-*.so.*
%{_libdir}/libxerces-*.so
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/libxerces-*.so.*
%{_libdir}/%{_arch64}/libxerces-*.so
%endif

%changelog
* Sun Feb 17 2008 - laca@sun.com
- create based on xerces-c.spec distributed with Xerces-C-2.8.0
