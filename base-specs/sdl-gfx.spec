#
# spec file for package SFEsdl-gfx
#
# includes module(s): SDL
#

%define src_name	SDL_gfx
%define src_url		http://www.ferzkopp.net/Software/%{src_name}-2.0

Name:			SFEsdl-gfx
Summary: 		Graphics library for SDL
Version:		2.0.16
Source: 		%{src_name}-%{version}.tar.gz
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
            --sysconfdir=%{_sysconfdir}		\
	    %mmx_option

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jun  5 2007 - Doug Scott
- Change to isabuild
* Tue May  8 2007 - Doug Scott
- Initial version
