#
# spec file for package SFEgmime
#
# includes module(s): gmime
#
%include Solaris.inc

Name:         SFEgmime
License:      Other
Version:      2.2.2
Release:      1
Distribution: N/A
Summary:      Libraries and binaries to parse and index mail messages
Source:       http://spruce.sourceforge.net/gmime/sources/v2.2/gmime-%{version}.tar.gz
URL:          http://spruce.sourceforge.net/gmime/
Patch1:       gmime-01-solaris.diff
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEmono-devel
Requires: SUNWgnome-base-libs
Requires: SFEmono

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -c -n %name-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

cd gmime-%{version}

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
			--enable-mono
make -j $CPUS

%install
cd gmime-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

# conflicts with SUNWesu
rm -f $RPM_BUILD_ROOT%{_bindir}/uuencode
rm -f $RPM_BUILD_ROOT%{_bindir}/uudecode

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %dir %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %dir %{_datadir}/gapi-2.0
%{_datadir}/gapi-2.0/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.sh
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%{_datadir}/gtk-doc

%changelog
* Sun Jul 13 2006 - laca@sun.com
- rename to SFEgmime
- include Solaris.inc
- correct patch file name, update CFLAGS, add gtk-docs to %files
* Wed Jul 12 2006 - jedy.wang@sun.com
- Initial spec
