#
# spec file for package kqemu
#
# includes module(s): kqemu
#

%define src_url http://www.opensolaris.org/os/project/kqemu/downloads

Name:		kqemu
Summary:	QEMU CPU Emulator Kernel module
Version:	1.0.3pre11-20070520
Source:		%{src_url}/%{name}_%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}_%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc

  
./configure --prefix=%{_prefix}	\
	    --cc=/usr/sfw/bin/gcc

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    make kqemu64
else
    make kqemu32
fi

%install
kdir=$RPM_BUILD_ROOT/%{_prefix}/kernel/drv
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    mkdir -p $kdir/%{_arch64}
    install -c kqemu-solaris-x86_64 $kdir/%{_arch64}/kqemu
else
    mkdir -p $kdir
    install -c kqemu-solaris-i386 $kdir/kqemu
    install -c kqemu.conf $kdir/kqemu.conf
fi


%changelog
* Mon Oct  8 2007 - dougs@truemail.co.th
- Initial version
