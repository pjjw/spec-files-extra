#
# spec file for package SFExmlrpc-c-gpp
#
# includes module(s): xmlrpc-c-gpp
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use xmlrpc_c = xmlrpc-c.spec

Name:                   SFExmlrpc-c-gpp
Summary:                A lightweight RPC library based on XML and HTTP (g++ version)
Version:                %{xmlrpc_c.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWgccruntime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%xmlrpc_c.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%{gcc_optflags}"
export LDFLAGS="%_ldflags"
%xmlrpc_c.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%xmlrpc_c.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sat May 24 2008 - trisk@acm.jhu.edu
- Initial spec
