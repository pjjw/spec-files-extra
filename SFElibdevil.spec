#
# spec file for package SFElibdevil.spec
#
# includes module(s): libdevil
#
%include Solaris.inc

%define src_name	DevIL
%define src_url		http://jaist.dl.sourceforge.net/sourceforge/openil

Name:                   SFElibdevil
Summary:                Cross-platform image library
Version:                1.6.8
Source:                 %{src_url}/%{src_name}-%{version}-rc2.tar.gz
patch1:			libdevil-01-wall.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibmng-devel
Requires: SFElibmng
BuildRequires: SFElcms-devel
Requires: SFElcms

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


libtoolize --force --copy
aclocal -I .
automake -a
autoconf --force
#export CFLAGS="$(echo %optflags|sed -e 's/-xpentium//' -e 's/-xspace//')"
export CFLAGS="-xO2"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-z muldefs"
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
export LD_OPTIONS="-z muldefs"
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
