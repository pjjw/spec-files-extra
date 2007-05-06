#
# spec file for package SFEggi.spec
#
# includes module(s): ggi
#
%include Solaris.inc

%include base.inc
%use libgii = libgii.spec
%use libgiigic = libgiigic.spec
%use libggi = libggi.spec
%use libggigcp = libggigcp.spec
%use libggimisc = libggimisc.spec
%use libggiwmh = libggiwmh.spec

Name:                   SFEggi
Summary:                General Graphics Interface
Version:                2.2.2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:         %summary - platform dependent files, / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%libgii.prep -d %name-%version/%{base_arch}
%libgiigic.prep -d %name-%version/%{base_arch}
%libggi.prep -d %name-%version/%{base_arch}
%libggigcp.prep -d %name-%version/%{base_arch}
%libggiwmh.prep -d %name-%version/%{base_arch}

%build
rm -rf $RPM_BUILD_ROOT
%libgii.build -d %name-%version/%{base_arch}
%libgii.install -d %name-%version/%{base_arch}

%libgiigic.build -d %name-%version/%{base_arch}
%libgiigic.install -d %name-%version/%{base_arch}

%libggi.build -d %name-%version/%{base_arch}
%libggi.install -d %name-%version/%{base_arch}

%libggigcp.build -d %name-%version/%{base_arch}
%libggigcp.install -d %name-%version/%{base_arch}

%libggiwmh.build -d %name-%version/%{base_arch}
%libggiwmh.install -d %name-%version/%{base_arch}

%install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%{_libdir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
