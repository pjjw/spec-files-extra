#
# spec file for package SFEnewt
#
# includes module(s): newt
#
%include Solaris.inc

Name:      SFEnewt
Summary:   Newt - A windowing toolkit for text mode built from the slang library
Version:   0.52.2
Source:	   http://archive.ubuntu.com/ubuntu/pool/main/n/newt/newt_%{version}.orig.tar.gz
Patch1:    newt-00-generic-fixes.diff
Patch2:    newt-01-solaris-fstat.diff
Patch3:    newt-02-solaris-makefile.diff
URL:       http://packages.ubuntu.com/intrepid/libnewt0.52
SUNW_BaseDir:  %{_basedir}
BuildRoot:  %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWslang
Requires: SUNWslang

%prep
%setup -q -n newt-%{version}
gzcat newt-%{version}.tar.gz | tar xvf -
cd newt-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
pwd
ls
cd newt-%{version}
autoreconf
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --datadir=%{_datadir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --includedir=%{_includedir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd newt-%{version}
make install instroot=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/libnewt.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libnewt.*
%{_libdir}/whiptcl.*
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%{_libdir}/python2.4/site-packages/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/newt.h

%changelog
* Fri Jun 20 2008 - river@wikimedia.org
- need to remove -Wall from makefile
- don't build 'depend' target as it only works with gcc
- change SFEslang to SUNWslang
* Thu May 01 2008 - ananth@sun.com
- Initial spec
