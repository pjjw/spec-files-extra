#
# spec file for package SFEfvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%include base.inc
%use fvwm = fvwm.spec

Name:                   SFEfvwm
Summary:                %{fvwm.summary}
Version:                %{fvwm.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEreadline-devel
Requires: SFEreadline
Requires: SFElibstroke

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%fvwm.prep -d %name-%version/%{base_arch}

%build
%fvwm.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%fvwm.install -d %name-%version/%{base_arch}
(
  cd $RPM_BUILD_ROOT%{_datadir}/locale
  mv sv_SE sv
  ln -s sv sv_SE
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/fvwm
%defattr (-, root, other)
%{_datadir}/locale

%changelog
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
