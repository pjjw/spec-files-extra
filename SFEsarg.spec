#
# spec file for package SFEsarg
#
%include Solaris.inc
%define source_name sarg

%define _basedir /
%define maindir /opt/sarg
%define _bindir /opt/sarg/bin
%define _mandir /opt/sarg/man
%define sys_conf_dir /opt/sarg/etc
%define html_dir /var/apache2/htdocs/sarg

Name:                    SFEsarg
Summary:                 Squid Analysis Report Generator
Version:                 2.2.3.1
Source:                  http://prdownloads.sourceforge.net/sarg/%{source_name}-%{version}.tar.gz
URL:                     http://sarg.sourceforge.net/sarg.php
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{source_name}-%{version}-build
%include default-depend.inc
Requires:                SFEsquid 

%prep
%setup -q -n %{source_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -mt -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lm -lsocket -lnsl"

./configure --bindir=%{_bindir}   		\
	    --mandir=%{_mandir}   		\
            --enable-sysconfdir=%{sys_conf_dir}	\
            --enable-htmldir=%{html_dir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -Dp -m0755 sarg %{buildroot}%{_bindir}/sarg
install -Dp -m0644 sarg.conf %{buildroot}%{sys_conf_dir}/sarg.conf
install -Dp -m0644 exclude_codes %{buildroot}%{sys_conf_dir}/exclude_codes
install -Dp -m0644 sarg.1 %{buildroot}%{_mandir}/man1/sarg.1
install -Dp -m0644 sarg.conf %{buildroot}%{sys_conf_dir}/httpd/conf.d/sarg.conf
install -Dp -m0644 css.tpl %{buildroot}%{html_dir}/www/sarg/sarg.css

cp -av fonts/ images/ languages/ %{buildroot}%{sys_conf_dir}/

### Clean up buildroot
rm -rf %{buildroot}%{_sysconfdir}/sarg/languages/.new

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{maindir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sarg
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%defattr (-, root, other)
%dir %attr (0755, root, sys) /opt
%dir %attr (0755, root, sys) %{sys_conf_dir}
%{sys_conf_dir}/*
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, other) %{html_dir}
%dir %attr (0755, root, other) %{html_dir}/www
%dir %attr (0755, root, other) %{html_dir}/www/sarg
%{html_dir}/www/sarg/*

%changelog
* Sun Oct 21 2007 - Petr Sobotka sobotkap@centrum.cz
- Initial commit
