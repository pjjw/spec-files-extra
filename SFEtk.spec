#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtk
Summary:             Tk - TCL GUI Toolkit
Version:             8.4.16
Source:              %{sf_download}/tcl/tk%{version}-src.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr
Requires: SUNWlibms
Requires: SUNWxwplt
Requires: SUNWxwrtl
Requires: SFEtcl

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n tk%version/unix

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tkConfig.sh
%{_libdir}/libtk*
%dir %attr (0755, root, bin) %{_libdir}/tk8.4
%{_libdir}/tk8.4/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, bin) %{_mandir}/mann
%{_mandir}/man1/*
%{_mandir}/mann/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Sep 29 2007 - dick@nagual.nl
- Bumped to version 8.4.16
* Wed Jul 11 2007 - dick@nagual.nl
- Bumped to version 8.4.15
* Sun Jun 03 2007 - dick@nagual.nl
- Corrected the location of the mann directory
* Mon May 28 2007 - dick@nagual.nl
- Initial spec
