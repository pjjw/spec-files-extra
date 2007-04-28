#
# spec file for package SFEdosbox.spec
#
# includes module(s): dosbox
#
%include Solaris.inc

%define src_name	dosbox
%define src_url		http://jaist.dl.sourceforge.net/sourceforge/dosbox

Name:                   SFEdosbox
Summary:                DOS emulator
Version:                0.70
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			dosbox-01-socket.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"

libtoolize 
aclocal
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

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
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Thu Apr 26 2006 - dougs@truemail.co.th
- Initial version
