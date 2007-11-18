#
# spec file for package SFElibatomic-ops
#
# includes module(s): libatomic-ops
#
%include Solaris.inc

%define	src_ver 1.2
%define	src_name libatomic_ops
%define	src_url	http://www.hpl.hp.com/research/linux/atomic_ops/download

Name:		SFElibatomic-ops
Summary:	library for atomic memory update operations
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Provides implementations for atomic memory update operations on a number of architectures. This allows direct use of these in reasonably portable code. Unlike earlier similar packages, this one explicitly considers memory barrier semantics, and allows the construction of code that involves minimum overhead across a variety of architectures.

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CFLAGS="-O4 -fno-omit-frame-pointer"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"

libtoolize --copy --force
aclocal
autoconf -f
autoheader
automake -a -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/libatomic_ops

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Change LDFLAGS to work for gcc.
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial spec
