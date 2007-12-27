%include Solaris.inc
%define pluginname favorites
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - favorites
# Version e.g. 0.15.5.0, note: gmpcplugin.gmpcmainversion is 0.15.5
Version:                %{gmpcplugin.version}
 

%prep
%gmpcplugin.prep
 
%build
%gmpcplugin.build
 
%install
%gmpcplugin.install

%clean
%gmpcplugin.clean

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gmpc
%dir %attr (0755, root, other) %{_datadir}/gmpc/plugins
%{_datadir}/gmpc/plugins/*


%changelog
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
