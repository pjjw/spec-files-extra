#
# spec file for package SFEneon
#
# includes module(s): neon
#
%include Solaris.inc

Name:			SFEneon
License:		LGPL
Group:			system/dscm
# Be careful not to update this to a newer version without checking
# if subversion will like it.
Version:		0.26.2
Release:		1
Summary:		neon http and webdav client library
Source:			http://www.webdav.org/neon/neon-%{version}.tar.gz
URL:			http://www.webdav.org/neon/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
%include default-depend.inc
Conflicts: SUNWneon
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWlexpt
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWsfwhea

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWbash

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n neon-%{version}

%build
export CFLAGS="%optflags -I/usr/sfw/include -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
%if %debug_build
%define debug_option --enable-debug
%else
%define debug_option --disable-debug
%endif
export CPPFLAGS="-I/usr/sfw/include"
export LD=/usr/ccs/bin/ld
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib -L$RPM_BUILD_ROOT%{_libdir}"
export PATH=$PATH:/usr/apache2/bin
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --disable-static \
    --enable-shared \
    --mandir=%{_mandir} \
    --with-ssl \
    --with-libxml2 \
    --infodir=%{_infodir} \
    %debug_option
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/neon-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Sat Jan 26 2008 - moinakg.ghosh@sun.com
- Fixed typo in conflict tag.
* Sat Jan 13 2008 - moinak.ghosh@sun.com
- Add conflict with SUNWneon
* Wed Mar 28 2007 - laca@sun.com
- unbump to 0.25.5 otherwise subversion refuses to build with dav support
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 0.26.3
- Add back l10n package
* Mon Nov  6 2006 - laca@sun.com
- delete l10n subpkg -- no l10n files
* Sat Oct 14 2006 - laca@sun.com
- initial version
