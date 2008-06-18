#
# spec file for package SFErtorrent
#
# includes module(s): rtorrent
#
%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/sfw/bin/g++
%include base.inc

%use rtorrent = rtorrent.spec
%use rlibtorrent = rlibtorrent.spec


Name:		SFErtorrent
Summary:	%{rtorrent.summary}
Version:	%{rtorrent.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
Requires: SFExmlrpc-c-gpp
BuildRequires: SFExmlrpc-c-gpp-devel
Requires: SUNWcurl
Requires: SFEncurses
BuildRequires: SFEncurses-devel

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%rlibtorrent.prep -d %name-%version/%{base_arch}
%rtorrent.prep -d %name-%version/%{base_arch}

%build
LIBTORRENT_ROOT=%{_builddir}/%name-%version/%{base_arch}/%{rlibtorrent.name}-%{rlibtorrent.version}
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags} -I/usr/gnu/include -I/usr/gnu/include/ncurses -I$LIBTORRENT_ROOT"/src
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -R%{_cxx_libdir} -L$LIBTORRENT_ROOT/src/.libs"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig:$LIBTORRENT_ROOT"
%rlibtorrent.build -d %name-%version/%{base_arch}
%rtorrent.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%rtorrent.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rtorrent
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/rtorrent.1

%changelog
* Sat May 24 2008 - trisk@acm.jhu.edu.
- Add SFExmlrpc-c-gpp dependencies
* Fri May  9 2008 - laca@sun.com
- Initial version
