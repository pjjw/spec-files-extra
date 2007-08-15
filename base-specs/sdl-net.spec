#
# spec file for package SFEsdl-net
#
# includes module(s): SDL
#

%define src_name	SDL_net
%define src_url		http://www.libsdl.org/projects/%{src_name}/release

Name:			sdl-image
Summary: 		Network library for SDL
Version:		1.2.7
Source: 		%{src_url}/%{src_name}-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
export PATH=%{_bindir}:$PATH
export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags" 
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Bump to 1.2.7
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Sun Apr 22 2007 - Doug Scott
- Initial version
