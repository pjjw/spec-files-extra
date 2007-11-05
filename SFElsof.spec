#
# spec file for package SFElsof
#
# includes module(s): lsof
#
# Risk alert: This package's main exectuable, /usr/bin/lsof, is set 
# gid (2755), with group-owner sys so it can read /dev/kmem.
#

%include Solaris.inc

Name:                SFElsof
Summary:             List open files
Version:             4.78
Source:              ftp://ftp.cerias.purdue.edu/pub/tools/unix/sysutils/lsof/lsof_%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n lsof_%version

%build 

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

tar -xf lsof_4.78_src.tar
cd lsof_4.78_src
export LSOF_VSTR=5.10
./Configure -n solariscc

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd lsof_4.78_src
install -D lsof $RPM_BUILD_ROOT%{_bindir}/lsof
install -D lsof.8   $RPM_BUILD_ROOT%{_mandir}/man8/lsof.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (2755, root, sys) %{_bindir}/lsof
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/lsof.8

%changelog
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 4.78.
* Sun Mar 18 2007 - Eric Boutilier
- Initial spec
