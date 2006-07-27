#
# spec file for package SFEsocks5
#
# includes module(s): socks5
#
%include Solaris.inc

Name:                    SFEsocks5
Summary:                 socks5
Version:                 v1.0r11
Source:                  http://freeware.sgi.com/source/socks5/socks5-%{version}.tar.gz
Patch1:                  socks5-01-varargs.diff
Patch2:                  socks5-02-manpath.diff
Patch3:                  socks5-03-perms.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n socks5-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_mandir}         \
	    --mandir=%{_mandir}         \
	    --libdir=%{_libdir}         \
	    --sysconfdir=%{_sysconfdir}
	    
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{_prefix} \
             mandir=$RPM_BUILD_ROOT/%{_mandir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a

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
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Tue Jul 25 2006 - laca@sun.com
- rename to SFEsocks5
- update file attributes
* Wed Mar 22 2006 - Darren.Kenny@Sun.COM
- Initial spec
