# 
# 
# 
%include Solaris.inc

#%define tcl_version 8.4
#%define tcl_8_3 %(pkgchk -l SUNWTcl 2>/dev/null | grep /usr/sfw/bin/tclsh8.3 >/dev/null && echo 1 || echo 0)

Name:                SFEalpine
License:             Apache
Summary:             University of Washington Alpine mail user agent
Version:             0.9999
Source:              ftp://ftp.cac.washington.edu/alpine/alpine-%{version}.tar.bz2
Patch1:              alpine-01-sunldap.diff
URL:                 http://www.washington.edu/alpine/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries
BuildRequires: SUNWhea
Requires: SUNWcsl
#BuildRequires: SUNWTcl

%prep
%setup -q -n alpine-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -mt -L/usr/sfw/lib -R/usr/sfw/lib"

#%if %tcl_8_3
#TCL_OPTS="--with-tcl-lib=tcl8.3"
#%else
#TCL_OPTS="--with-tcl-lib=tcl%{tcl_version}"
#%endif
TCL_OPTS=

autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-system-pinerc=%{_sysconfdir}/pine.conf \
	    --with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed \
            --with-passfile=.pine-passfile \
            --disable-debug \
            --with-debug-level=0 \
            $TCL_OPTS

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

for prog in pico pilot rpdump rpload; do
	mv $RPM_BUILD_ROOT%{_bindir}/$prog $RPM_BUILD_ROOT%{_bindir}/alpine-$prog
	mv $RPM_BUILD_ROOT%{_mandir}/man1/$prog.1 $RPM_BUILD_ROOT%{_mandir}/man1/alpine-$prog.1
done

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
* Mon Oct 08 2007 - trisk@acm.jhu.edu
- Initial spec, should be friendly with SFEpine