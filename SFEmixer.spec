#
# spec file for package SFEmixer
#
# includes module(s): mixer
#
%include Solaris.inc

Name:                    SFEmixer
Summary:                 Command line audio mixer
Version:                 1.2
Source:			 http://softagalleria.net/download/mixer/mixer-%{version}.tar.gz
URL:                     http://softagalleria.net/mixer.php
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWaudh

%prep
%setup -q -n mixer-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
$CC $CFLAGS $LDFLAGS mixer.c -o mixer

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
cp -p mixer $RPM_BUILD_ROOT%{_prefix}/bin/mixer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Mon Feb 25 2007 - trisk@acm.jhu.edu
- Initial spec
