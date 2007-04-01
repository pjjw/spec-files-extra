#
# spec file for package SFEsdl-image
#
# includes module(s): SDL
#
%include Solaris.inc

Summary: Simple DirectMedia Layer - Sample Image Loading Library
Name:			SFEsdl-image 
Version:		1.2.5 
Source: 		http://www.libsdl.org/projects/SDL_image/release/SDL_image-%{version}.tar.gz
License: LGPL
SUNW_BaseDir:			%{_basedir}
BuildRoot:			%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n SDL_image-%version

#BuildRequires: SDL-devel
#BuildRequires: libjpeg-devel
#BuildRequires: libpng-devel
#BuildRequires: libtiff-devel

%description
This is a simple library to load images of various formats as SDL surfaces.
This library supports BMP, PPM, PCX, GIF, JPEG, PNG, and TIFF formats.

%package devel
Summary: Libraries, includes and more to develop SDL applications.
Group: Development/Libraries
SUNW_BaseDir:		%{_basedir}
%include default-depend.inc
Requires: %{name}
Requires: SFEsdl-devel

%description devel
This is a simple library to load images of various formats as SDL surfaces.
This library supports BMP, PPM, PCX, GIF, JPEG, PNG, and TIFF formats.

%prep
rm -rf ${RPM_BUILD_ROOT}

%build
CFLAGS="$RPM_OPT_FLAGS" 
./configure --prefix=%{_prefix}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%doc README CHANGES COPYING
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/SDL/

%changelog
* Sun Apr 01 2007 Jeff Cai
- Initial version

