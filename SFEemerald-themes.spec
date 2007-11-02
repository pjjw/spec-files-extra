#
# spec file for package SFEemerald-themes
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.


%include Solaris.inc

%define src_name emerald-themes

Name:                    SFEemerald-themes
Summary:                 themes for the emerald compiz window decorator 
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2	 
Patch1:			 emerald-themes-01-solaris-port.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, sys)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/emerald
%{_datadir}/emerald/*


%changelog
* Thu Nov 01 2007 - trisk@acm.jhu.edu
- Fix permissions
* Fri Sep 11 2007 - erwann@sun.com
- Initial spec
