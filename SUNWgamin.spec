#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include base.inc
%use gamin = gamin.spec

# The the following is quite a bit hacky.  It is due to historic reasons.
# libnotify was first introduced in SFE as SFElibnotify but it was later
# moved to Xfce as OSOLlibnotify, then even later it became part of JDS
# and included in SUNWgnome-panel.
# If /usr/lib/libnotify.so is found on the system, it is assumed that it
# comes from JDS.  If not, this package will require OSOLlibnotify
%define libnotify_installed %(test -f /usr/lib/libnotify.so && echo 1 || echo 0)

Name:			OSOLgamin
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
* Sun Apr 15 2007 - dougs@truemail.co.th
- Initial version
