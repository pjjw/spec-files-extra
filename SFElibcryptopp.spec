#
# spec file for package SFElibcryptocpp.spec
#
# includes module(s): libcryptopp
#
%include Solaris.inc

%define src_name	cryptopp
%define src_version	551
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg:	SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	${src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:                   SFElibcryptopp
Summary:                libcrypto++ - C++ class library of cryptographic algorithms
Version:                551
Source:                 %{src_url}/%{src_name}%{version}.zip
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms
#BuildRequires: 

%prep
%setup -c -q -n %{src_name}%{version}

%build
export CC=/opt/SUNWspro/bin/cc
export CXX=/opt/SUNWspro/bin/CC
make 

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT%{_basedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,bin) %{_includedir}
%{_includedir}/*

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

