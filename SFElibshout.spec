#
# spec file for package SFElibshout.spec
#
# includes module(s): libshout
#

%include Solaris.inc

%define src_name	libshout
%define src_url		http://downloads.xiph.org/releases/libshout

Name:                   SFElibshout
Summary:                libshout, Library which can be used to write a source client like ices
Version:                2.2.2
Source:                 %{src_url}/libshout-%{version}.tar.gz
SUNW_BaseDir:           /
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFWoggl
BuildRequires: SUNWlibtheora-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWlxsl-devel
BuildRequires: SUNWogg-vorbis-devel
# TODO needed? BuildRequires: SUNWspeex-devel
Requires: SFWoggl
Requires: SUNWlibtheora
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWogg-vorbis
# TODO needed? Requires: SUNWspeex

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name



%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP -D_AVL_H"
export LDFLAGS="%_ldflags"

./configure --prefix=/usr               \
            --bindir=/usr/bin           \
            --mandir=/usr/share/man     \
            --libdir=/usr/lib           \
            --datadir=/usr/share        \
            --libexecdir=/usr/lib       \
            --sysconfdir=/etc           \
            --enable-shared             \
            --disable-static            \

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rmdir $RPM_BUILD_ROOT%{_bindir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
#below: usr/bin was created but never installed
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*



%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*



%changelog
* Tue May 8 2007 - Thomas Wagner
- Initial version