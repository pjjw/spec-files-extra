#
# spec file for package SFEleafpad
#
# includes module(s): leafpad
#
%include Solaris.inc

Name:                    SFEleafpad
Summary:                 Leafpad GTK+ based text editor.
Version:                 0.8.13
Source:                  http://savannah.nongnu.org/download/leafpad/leafpad-%{version}.tar.gz
URL:                     http://tarot.freeshell.org/leafpad/
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n leafpad-%version

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
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_datadir}
%{_datadir}/*

%changelog
* Sat Dec 23 2007 - pradhap (at) gmail.com
- Initial leafpad spec file

