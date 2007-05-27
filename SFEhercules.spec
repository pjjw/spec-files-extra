#
# spec file for package SFEhercules.spec
#
# includes module(s): hercules
#
%include Solaris.inc

%define src_name	hercules
%define src_url		http://www.hercules-390.org

Name:                   SFEhercules
Summary:                Mainframe Emulator
Version:                3.04.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			hercules-01-wall.diff
Patch2:			hercules-02-solaris.diff
Patch3:			hercules-03-test_cmd.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


#libtoolize --force
aclocal -I m4 -I autoconf
autoheader
automake --add-missing
autoconf --force

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
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/hercules
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/hercules
%{_mandir}

%changelog
* Sun May 28 2007 - dougs@truemail.co.th
- Initial version
