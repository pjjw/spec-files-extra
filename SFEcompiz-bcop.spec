#
# spec file for package SFEcompiz-bcop
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

####################################################################
#  beryl compiz XML option parser
####################################################################

%include Solaris.inc

Name:                    SFEcompiz-bcop
Summary:                 beryl compiz XML option parser
Version:                 0.5.2
Source:			 http://releases.compiz-fusion.org/0.5.2/compiz-bcop-%{version}.tar.bz2
Patch1:			 compiz-bcop-01-solaris-port.pc
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:		 SFEgetopt
%include default-depend.inc


%prep
%setup -q -c -n %name-%version
%patch1 -p1

%build
cd compiz-bcop-%{version}
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal
autoheader
automake -a -c -f
autoconf

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{_ldflags}"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
	    --with-getopt=/usr/gnu/bin/getopt

make -j$CPUS

%install
cd compiz-bcop-%{version}
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Tue Aug 28 2007 - erwann@sun.com
- init spec for the new package format
