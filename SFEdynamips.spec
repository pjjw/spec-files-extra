#
# spec file for package SUNWdynamips.spec
#
# gcc only for now

%include Solaris.inc

Name:                    SFEdynamips
Summary:                 dynamips - Cisco 7200 Simulator
Group:			 System/Emulator
SUNW_Copyright:      	 %{name}.copyright
Version:                 0.2.7
Source:			 http://www.ipflow.utc.fr/dynamips/dynamips-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibpcap
Patch1:                 dynamips-01-makefile.diff
#Patch2:			dynamips-02-makefile-suncc.diff

%prep
%setup -q -n dynamips-%version
%patch1 -p0
#%if %cc_is_gcc
#%else
#%patch2 -p0
#%endif

%build
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

make 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/usr install
rmdir $RPM_BUILD_ROOT/usr/etc
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{name}
install -m644 COPYING $RPM_BUILD_ROOT/usr/share/doc/%{name}
install -m644 README  $RPM_BUILD_ROOT/usr/share/doc/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) /usr/share
%{_mandir}/*/*
%dir %attr (0755, root, other) /usr/share/doc
%dir %attr (0755, root, bin) /usr/share/doc/%{name}
/usr/share/doc/%{name}/*

%changelog
* Mon Nov 24 2008 - sergiusens@ieee.org
- Initial spec file, gcc only
