#
# spec file for package SFExmlrpc-c
#
# includes module(s): xmlrpc-c
#
%include Solaris.inc

%include base.inc

%use xmlrpc_c = xmlrpc-c.spec

Name:                   SFExmlrpc-c
Summary:                A lightweight RPC library based on XML and HTTP
Version:                %{xmlrpc_c.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

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
export CFLAGS="%optflags"
export CFLAGS_PERSONAL="%optflags"
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
* Tue Jun 24 2008 - trisk@acm.jhu.edu
- Rename to SFExmlrpc-c since we don't distribute C++ libs
- Add CFLAGS_PERSONAL for Studio
* Sat May 24 2008 - trisk@acm.jhu.edu
- Initial spec
