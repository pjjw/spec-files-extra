#
# Notes: 
# - This spec file will only work if CC is gcc. Do it at the command line
#   before invoking this spec file (as opposed to putting it in %build below).
#   That way the macros in Solaris.inc will know you've set it
#
# - There's a widely used, long-standing patch that gets this source to
#   build a shared library. I have not applied it here. It'd be 
#   great if the libnet developer(s) would incorporate it upstream...
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibnet
Summary:             Packet Construction Library
Version:             1.1.2.1
Source:              http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n libnet

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

# Following is a hack that comments out these lines in libnet_link_dlpi.c:
#
# if (*eos != '\0')
# {
#     snprintf(l->err_buf, LIBNET_ERRBUF_SIZE,
#             "%s(): %s bad unit number\n", __func__, l->device);
#     goto bad;
# }

perl -i.orig -lne 'print q!/*! if $.==142;print q!*/! if $.==148;print' src/libnet_link_dlpi.c 

# It was done because a bug here makes libnet (and therefore ettercap) 
# think that the e1000g0 interface on my laptop is invalid causing ettercap
# to fatally exit as a result. Beware: this means the intent for the ommited
# code is now being circumvented.

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* 
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
