#
# spec file for package qemu
#
# includes module(s): qemu
#

%define src_url http://www.opensolaris.org/os/project/qemu/downloads

Name:		qemu
Summary:	QEMU CPU Emulator
Version:	20070612
Source:		%{src_url}/qemu-CVS-%{version}-patched.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n qemu

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4"
export LDFLAGS="%{_ldflags}"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  export PATH=/usr/sfw/bin:/opt/jdsbuild/bin:/usr/bin/amd64:$PATH
  qemuopts="--target-list=x86_64-softmmu,i386-softmmu"
else
  qemuopts="--force-32bit --target-list=i386-softmmu"
fi

./configure --prefix=%{_prefix} \
	    $qemuopts
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT/%{_prefix}/bin/qemu $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT/%{_prefix}/bin/qemu-img $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT/%{_prefix}/bin/qemu-system-x86_64 $RPM_BUILD_ROOT/%{_bindir}
fi

%changelog
* Mon Oct  8 2007 - dougs@truemail.co.th
- Initial version
