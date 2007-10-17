#
# spec file for package SFEqemu
#
# includes module(s): qemu
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use qemu64 = qemu.spec
%use kqemu64 = kqemu.spec
%endif

%include base.inc
%use qemu = qemu.spec
%use kqemu = kqemu.spec

Name:		SFEqemu
Summary:	%{qemu.summary}
Version:	%{qemu.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%qemu64.prep -d %name-%version/%_arch64
%kqemu64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%qemu.prep -d %name-%version/%{base_arch}
%kqemu.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%qemu64.build -d %name-%version/%_arch64
%kqemu64.build -d %name-%version/%_arch64
%endif

%qemu.build -d %name-%version/%{base_arch}
%kqemu.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%qemu64.install -d %name-%version/%_arch64
%kqemu64.install -d %name-%version/%_arch64
%endif

%qemu.install -d %name-%version/%{base_arch}
%kqemu.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
	
	perl -ni -e 'print unless /name=kqemu/' /etc/devlink.tab
	printf "type=ddi_pseudo;name=kqemu\t\\D\n" >> /etc/devlink.tab
	add_drv kqemu
)

%postun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
	
	rem_drv kqemu
	perl -ni -e 'print unless /name=kqemu/' /etc/devlink.tab
	rm /dev/kqemu
)

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/qemu
%{_bindir}/qemu-img
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qemu
%dir %attr (0755, root, sys)  %{_prefix}/kernel
%dir %attr (0755, root, sys)  %{_prefix}/kernel/drv
%attr (0644, root, sys) %{_prefix}/kernel/drv/kqemu
%attr (0644, root, sys) %{_prefix}/kernel/drv/kqemu.conf
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/qemu
%{_bindir}/%{_arch64}/qemu-img
%{_bindir}/%{_arch64}/qemu-system-x86_64
%dir %attr (0755, root, sys) %{_prefix}/kernel/drv/%{_arch64}
%attr (0644, root, sys) %{_prefix}/kernel/drv/%{_arch64}/kqemu
%endif

%changelog
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial version
