#
# spec file for package SFEsdl-gfx
#
# includes module(s): SDL
#
%include Solaris.inc

%define sdl_name	SDL_gfx
Name:			SFEsdl-gfx
Summary: 		Graphics library for SDL
Version:		2.0.16
Source: 		http://www.ferzkopp.net/Software/%{sdl_name}-2.0/%{sdl_name}-%{version}.tar.gz
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl

%prep
%setup -q -n %{sdl_name}-%{version}

%package devel
Summary: Libraries, includes and more to develop SDL applications.
Group: Development/Libraries
SUNW_BaseDir:		%{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf ${RPM_BUILD_ROOT}

%build
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags" 
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}		\
	    --disable-mmx

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
%{_libdir}/lib*.so*

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/SDL/

%changelog
* Tue May  8 2007 - Doug Scott
- Initial version
