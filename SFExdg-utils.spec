#
# spec file for package SFExdg-utils
#
# includes module(s): xdg-utils
#

%include Solaris.inc

Name:                SFExdg-utils
Summary:             The Portland Project's desktop integration tools
Version:             1.0.2
Source:              http://portland.freedesktop.org/download/xdg-utils-%{version}.tgz
Patch0:              xdg-utils-01-bash.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n xdg-utils-%{version}
%patch0 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} 

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}

%changelog
* Sat Oct 06 2007 - ananth@sun.com
- Initial spec
