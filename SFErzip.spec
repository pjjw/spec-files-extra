#
# spec file for package SFErzip
#
# includes module(s): rzip
#
%include Solaris.inc

Name:                    SFErzip
Summary:                 rzip, a compression program using extremely large windows
Version:                 2.1
Source:	                 http://rzip.samba.org/ftp/rzip/rzip-%{version}.tar.gz
Patch1:                  rzip-01-makefile.diff
Patch2:                  rzip-02-maintain_times.diff
URL:                     http://rzip.samba.org/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWbzip
Requires: SUNWbzip

%prep
%setup -q -n rzip-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Thu Apr 17 2008 - trisk@acm.jhu.edu
- Initial spec
