#
# spec file for package electric-fence
#
# includes module(s): electric-fence
#

%define	src_ver 2.1.13
%define tarball_version %{src_ver}-0.1
%define	src_name electric-fence
%define	src_url	http://perens.com/FreeSoftware/ElectricFence

Name:		electric-fence
Summary:	A debugger which detects memory allocation violations
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}_%{tarball_version}.tar.gz
Patch1:		electric-fence-01-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
If you know what malloc() violations are, you'll be interested in
ElectricFence. ElectricFence is a tool which can be used for C
programming and debugging. It uses the virtual memory hardware of your
system to detect when software overruns malloc() buffer boundaries,
and/or to detect any accesses of memory released by free().
ElectricFence will then stop the program on the first instruction that
caused a bounds violation and you can use your favorite debugger to
display the offending statement.

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags %picflags"
export LDFLAGS="%_ldflags"

LIBDIR=%{_libdir} \
MANDIR=%{_mandir} \
make

%install
LIBDIR=%{_libdir} \
MANDIR=%{_mandir} \
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial spec
