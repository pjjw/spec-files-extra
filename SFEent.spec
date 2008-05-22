#
# spec file for package SFEent
#
# includes module(s): ent (random)
#
%include Solaris.inc

Name:                SFEent
Summary:             ent - Pseudorandom Number Sequence Test Program
Version:             3.14
Source:              http://www.fourmilab.ch/random/random.zip
URL:                 http://www.fourmilab.ch/random/
SUNW_Copyright:      %{name}.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %name-%version

%build
make CC="$CC" CFLAGS="%optflags"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 ent  $RPM_BUILD_ROOT%{_bindir}

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/ent

%changelog
* Thu May 22 2008 - laca@sun.com
- Initial spec
