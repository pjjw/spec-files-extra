#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Note: This spec file will only work if CC is gcc. Do it at the command line
# before invoking this spec file (as opposed to putting it in %build below).
# That way the macros in Solaris.inc will know you've set it (I think).

%include Solaris.inc

Name:                SFErrdtool
Summary:             Data analysis tool generating graphical representations
Version:             1.2.15
Source:              http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/pub/rrdtool-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n rrdtool-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"


# I punted on building w/ perl and python enabled. IOW, this
# spec file is in need of someone (perhaps an rrdtool
# aficionado?) to give it some proper TLC.

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --disable-perl \
            --disable-python \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* 
* Fri Sep 20 2006 - Eric Boutilier
- Initial spec
