# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use gamin = gamin.spec

Name:			SUNWgamin
Summary:		%{gamin.summary}
Version:		%{gamin.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:		%{summary} - developer files
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
Requires:		%{name}

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%gamin.prep -d %name-%version/%base_arch

%build
%gamin.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%gamin.install -d %name-%version/%base_arch

# move python stuff to vendor-packages
(
  cd $RPM_BUILD_ROOT%{_libdir}/python*
  mv site-packages vendor-packages
  rm vendor-packages/*.la
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libexecdir}/gam_server
%{_libdir}/python2.4/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
* Sat Oct 13 2007 - lin.ma@sun.com
- Initial FEN backend
* Sun Apr 15 2007 - dougs@truemail.co.th
- Initial version
