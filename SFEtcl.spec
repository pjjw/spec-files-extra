#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtcl
Summary:             Tcl - Tool Command Language
Version:             8.4.14
Source:              http://prdownloads.sourceforge.net/tcl/tcl%{version}-src.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr
Requires: SUNWlibms
Requires: SUNWgcmn

%prep
%setup -q -n tcl%version/unix

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export CFLAGS="%optflags"
#export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	    --enable-shared \
	    --enable-threads

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
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tclConfig.sh
%{_libdir}/libtcl*
%dir %attr (0755, root, bin) %{_libdir}/tcl8.4
%{_libdir}/tcl8.4/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Mon May 28 2007 - dick@nagual.nl
- Initial spec
