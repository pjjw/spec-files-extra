#
# spec file for package SFEaterm.spec
#
# includes module(s): aterm
#
%include Solaris.inc

%include base.inc
%use aterm = aterm.spec

Name:                   SFEaterm
Summary:                %{aterm.summary}
Version:                %{aterm.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEafterstep-devel
Requires: SFEafterstep

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%aterm.prep -d %name-%version/%{base_arch}

%build
export CC=/usr/sfw/bin/gcc
%aterm.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%aterm.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}

%changelog
* Sat Apr 28 2007 - dougs@truemail.co.th
- Initial version
