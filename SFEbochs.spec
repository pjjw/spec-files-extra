#
# spec file for package SFEbochs.spec
#
# includes module(s): bochs
#
%include Solaris.inc

%define src_name	bochs
%define src_url		http://%{src_name}.sourceforge.net/cvs-snapshot

Name:                   SFEbochs
Summary:                IA32 emulator
Version:                20080209
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEwxwidgets-devel
Requires: SFEwxwidgets

%prep
%setup -q -n %{src_name}-%{version}

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

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoconf --force

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --localedir=%{_datadir}/locale	\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
            --enable-shared			\
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
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/bochs

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 20080209
* Sat Apr 28 2006 - dougs@truemail.co.th
- Initial version
