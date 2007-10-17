#
# spec file for package SFEsdl-Pango
#
# includes module(s): SDL
#

%define src_name	SDL_Pango
%define src_url		http://%{sf_mirror}/sdlpango

Name:			sdl-Pango
Summary: 		Simple DirectMedia Layer - Pango Link Library
Version:		0.1.2
Source: 		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			sdl-pango-01-api-adds.diff
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

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
- Add patch for extended API
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial version
