#
# spec file for package SFEantlr.spec
#
# includes module(s): antlr
#
%include Solaris.inc

%define src_name	antlr
%define src_url		http://www.antlr.org/download

Name:                   SFEantlr
Summary:                ANother Tool for Language Recognition
Version:                3.0.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			antlr-01-destdir.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEmono-devel
Requires: SFEmono

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_sbindir}
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/%{src_name}-%{version}

%files devel
%defattr (-, root, bin)
%{_includedir}
%{_libdir}
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Oct 14 2007 - laca@sun.com
- bump to 3.0.1
* Sun May 13 2007 - dougs@truemail.co.th
- Initial version
