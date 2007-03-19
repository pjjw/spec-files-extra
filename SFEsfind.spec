#
# spec file for package SFEsfind
#
# includes module(s): sfind
#
%include Solaris.inc

Name:                SFEsfind
Summary:             fast POSIX-compliant tar
Version:             1.2
Source:              ftp://ftp.berlios.de/pub/sfind/sfind-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n sfind-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

/usr/ccs/bin/make

%install

export INS_BASE=$RPM_BUILD_ROOT%{_prefix}
export MANDIR=share/man
export DEFUMASK=022

rm -rf $RPM_BUILD_ROOT

/usr/ccs/bin/make -e install

rm -rf ${RPM_BUILD_ROOT}%{_libdir}
rm -rf ${RPM_BUILD_ROOT}%{_includedir}
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man4

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sfind
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/sfind.1

%changelog
* 
* Sun Mar 18 2007 - Eric Boutilier
- Initial spec
