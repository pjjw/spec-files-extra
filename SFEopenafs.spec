#
# spec file for package SFEopenafs.spec
#
%include Solaris.inc

# Place it in /opt
%define _basedir /opt/openafs
%define _bindir %{_basedir}/bin
%define _datadir %{_basedir}/share
%define _mandir %{_datadir}/man
%define _libdir %{_basedir}/lib

%define src_name openafs

Name:                    	SFEopenafs
Summary:                 	Distribuated file system.
Version:                 	1.4.5
Source:                  	http://openafs.org/dl/openafs/1.4.5/%{src_name}-%{version}-src.tar.bz2
BuildRoot:                      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:		SUNWhea

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export KRB5CFLAGS="-I/usr/include/kerberosv5"
export KRB5LIBS="/usr/lib/gss/mech_krb5.so -R/usr/lib/gss"

./configure --prefix=%{_basedir}			\
            --bindir=%{_bindir}				\
            --datadir=%{_datadir}			\
            --mandir=%{_mandir}				\
            --libdir=%{_libdir}				\
    	    --with-krb5=yes

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, other) %{_basedir}/include
%{_basedir}/include/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%defattr (0755, root, sys)
%dir %attr (0755, root, sys) %{_basedir}/libexec
%{_basedir}/libexec/*
%dir %attr (0755, root, sys) %{_basedir}/sbin
%{_basedir}/sbin/*

%changelog
* Mon Nov 26 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
