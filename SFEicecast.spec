#
# spec file for package SFEicecast.spec
#
# includes module(s): icecast


%include Solaris.inc

%define src_name	icecast
%define src_url		http://downloads.xiph.org/releases/icecast

Name:                   SFEicecast
Summary:                icecast, free server software for streaming multimedia
Version:                2.3.1
Source:                 %{src_url}/icecast-%{version}.tar.gz
Patch1:                 icecast-01-CURLOPT_PASSWDFUNCTION.diff 
SUNW_BaseDir:           /
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEcurl-devel
BuildRequires: SFWoggl
BuildRequires: SUNWlibtheora-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWlxsl-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWspeex-devel
BuildRequires: SUNWzlib
Requires: SFEcurl
Requires: SFWoggl
Requires: SUNWlibtheora
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWogg-vorbis
Requires: SUNWopenssl-libraries
Requires: SUNWspeex
Requires: SUNWzlib


%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


./configure --prefix=/usr               \
            --bindir=/usr/bin           \
            --mandir=/usr/share/man     \
            --libdir=/usr/lib           \
            --datadir=/usr/share        \
            --libexecdir=/usr/lib       \
            --sysconfdir=/etc           \
            --enable-shared             \
            --disable-static            \
            --with-vorbis=/usr  

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

#TODO: doc-section should be cleaned up (2xdoc)
%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/icecast
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/icecast
%dir %attr (0755, root, other) %{_datadir}/icecast/doc
%{_datadir}/icecast/doc/*
%dir %attr (0755, root, other) %{_datadir}/icecast/web
%{_datadir}/icecast/web/*
%dir %attr (0755, root, other) %{_datadir}/icecast/admin
%{_datadir}/icecast/admin/*


%changelog
* Tue May 8 2007 - Thomas Wagner
- Initial version
