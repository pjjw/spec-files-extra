#
# spec file for package SFEwindowmaker
#
#
%include Solaris.inc

Name:                    SFEwindowmaker
Summary:                 Windowmaker Your Next Window Manager
Version:                 0.92.0
Source:                  ftp://windowmaker.info/pub/source/release/WindowMaker-%{version}.tar.bz2
URL:                     http://www.windowmaker.info/ 
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n WindowMaker-%version

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

make

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_libdir}
%dir %attr(0755, root, bin) %{_libdir}/locale
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/sk
%{_mandir}/sk/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/WindowMaker
%{_datadir}/WindowMaker/*
%dir %attr(0755, root, bin) %{_datadir}/WPrefs
%{_datadir}/WPrefs/*
%dir %attr(0755, root, bin) %{_datadir}/WINGs
%{_datadir}/WINGs/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Fixed directory attributes
- Fri Dec 12 2007 - pradhap (at) gmail.com
- Initial Windowmaker spec file

