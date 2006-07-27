#
# spec file for package SFExrestop
#
# includes module(s): xrestop
#
%include Solaris.inc

Name:                    SFExrestop
Summary:                 xrestop - display X-Resource statistics
Version:                 0.4
Source:                  http://projects.o-hand.com/sources/xrestop/xrestop-%{version}.tar.gz
URL:                     http://www.freedesktop.org/wiki/Software_2fxrestop
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxwplt
Requires: SUNWxwrtl

%prep
%setup -q -n xrestop-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

%define xrestop_prefix	       %{_basedir}/X11
%define xrestop_bindir         %{xrestop_prefix}/bin
%define xrestop_libdir         %{xrestop_prefix}/lib
%define xrestop_libexecdir     %{xrestop_prefix}/lib
%define xrestop_includedir     %{xrestop_prefix}/include
%define xrestop_sysconfdir     /etc
%define xrestop_datadir        %{xrestop_prefix}/share
%define xrestop_mandir         %{xrestop_datadir}/man

./configure --prefix=%{xrestop_prefix}			\
	    --mandir=%{xrestop_mandir}			\
            --libdir=%{xrestop_libdir}			\
            --libexecdir=%{xrestop_libexecdir}		\
            --sysconfdir=%{xrestop_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{xrestop_bindir}
%{xrestop_bindir}/*
%dir %attr (0755, root, bin) %{xrestop_datadir}
%dir %attr(0755, root, bin) %{xrestop_mandir}
%dir %attr(0755, root, bin) %{xrestop_mandir}/man1
%{xrestop_mandir}/man1/*

%changelog
* Fri Jun 30 2006 - laca@sun.com
- bump to 0.4
- rename to SFExrestop
- remove unnecessary env variables
* Wed Dec  7 2005 - glynn.foster@sun.com
- Initial spec
