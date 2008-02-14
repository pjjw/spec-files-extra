#
# spec file for package SFExdelta
#
%include Solaris.inc
%define src_name xdelta
%define src_ver 3.0t

Name:                    SFExdelta
Summary:                 Opensource binary diff 
Version:                 3.0
Source:                  http://xdelta.googlecode.com/files/%{src_name}%{src_ver}.tar.gz
URL:                     http://xdelta.org/
Patch1:					 xdelta-01-fixmakefile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}%{src_ver}-build
%include default-depend.inc

%prep
%setup -q -n "%{src_name}%{src_ver}"
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -mt -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp xdelta3 $RPM_BUILD_ROOT/usr/bin/xdelta3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Thu Feb 14 2007 - Petr Sobotka sobotkap@centrum.cz
- Initial version
