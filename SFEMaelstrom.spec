#
# spec file for package SFEMaelstrom
#
# includes module(s): Maelstrom
#
%include Solaris.inc
%use Maelstrom = Maelstrom.spec

Name:                    SFEMaelstrom
Summary:                 %{Maelstrom.summary}
Version:                 %{Maelstrom.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%Maelstrom.prep -d %name-%version

%build

%Maelstrom.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%Maelstrom.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/Maelstrom
%{_bindir}/Maelstrom-netd
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/Maelstrom
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop

%files root
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/games

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial version
