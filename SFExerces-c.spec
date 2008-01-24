#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define dirname xerces-c

Name:                SFExerces-c
Summary:             Xerces-C++ validating XML parser
Version:             2_8_0
Release:             3
Source:              http://apache.mirrors.tds.net/xerces/c/sources/xerces-c-src_%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{dirname}-%{version}-build
%include default-depend.inc
BuildRequires: SFEdoxygen

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The parser provides high performance, modularity, and scalability. Source
code, samples and API documentation are provided with the parser. For
portability, care has been taken to make minimal use of templates, no RTTI,
and minimal use of #ifdefs.

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen

%description devel
Header files you can use to develop XML applications with Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%package doc
Summary:        %{summary} - documentation
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%description doc
Documentation for Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%prep
%setup -q -n %{dirname}-src_%{version}

%build
export XERCESCROOT=$RPM_BUILD_DIR/%{dirname}-src_%{version}
cd $XERCESCROOT/src/xercesc

./runConfigure -p solaris -c gcc -x g++ -r pthread -P %{_prefix} -z "-I$XERCESCROOT/src"
gmake 
cd $XERCESCROOT/samples
./runConfigure -p solaris -c gcc -x g++
gmake 
cd $XERCESCROOT/doc
doxygen

%install
rm -rf $RPM_BUILD_ROOT
export XERCESCROOT=$RPM_BUILD_DIR/%{dirname}-src_%{version}
cd $XERCESCROOT/src/xercesc
gmake PREFIX=$RPM_BUILD_ROOT%{_prefix} install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin

# We don't want obj directory
install `find $XERCESCROOT/bin/* -prune -type f` $RPM_BUILD_ROOT%{_prefix}/bin
install -d $RPM_BUILD_ROOT%{_datadir}/%{dirname}
cp -a $XERCESCROOT/samples $RPM_BUILD_ROOT%{_datadir}/%{dirname}
install -d $RPM_BUILD_ROOT%{_datadir}/doc
install -d $RPM_BUILD_ROOT%{_datadir}/doc/%{dirname}
install $XERCESCROOT/LICENSE $RPM_BUILD_ROOT%{_datadir}/doc/%{dirname}
install $XERCESCROOT/NOTICE $RPM_BUILD_ROOT%{_datadir}/doc/%{dirname}
install $XERCESCROOT/STATUS $RPM_BUILD_ROOT%{_datadir}/doc/%{dirname}
install $XERCESCROOT/credits.txt $RPM_BUILD_ROOT%{_datadir}/doc/%{dirname}
cd $XERCESCROOT/doc
find . -name "*.html" | cpio -pdumv $RPM_BUILD_ROOT%{_datadir}/doc/%{dirname}

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/%{dirname}
%{_datadir}/%{dirname}/*

%files doc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Initial spec.
