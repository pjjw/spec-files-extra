#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEpan
Summary:             A newsreader for GNOME
Version:             0.14.2
Source:              http://pan.rebelbase.com/download/releases/%{version}/SOURCE/pan-%{version}.tar.gz
Patch1:              pan-01-gcclvalues.diff
Patch2:              pan-02-libm.diff
Patch3:              pan-03-gnet-ipv6.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Requires:
BuildRequires: SFEgnet-devel
Requires: SFEgnet

%prep
%setup -q -n pan-%version
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
	    --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
mv $RPM_BUILD_ROOT/%{_prefix}/share/gnome/apps/Internet/pan.desktop $RPM_BUILD_ROOT/%{_datadir}/applications
rm -rf  $RPM_BUILD_ROOT/%{_prefix}/share/gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Wed Jun 25 2008 - river@wikimedia.org
- add patch pan-03-gnet-ipv6.diff to fix GNet autodetect of ipv4/ipv6;
  causes all connections (v4 and v6) to fail unless a policy is forced.
* Mon Jun 23 2008 - river@wikimedia.org
- Initial spec
