#
# spec file for package unrar
#
# includes module(s): unrar
#

Name:                    unrar
Summary:                 Unrar Decompressor
Version:                 3.5.4
Source:                  http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz
URL:                     http://www.rarlab.com/
Patch1:			 unrar.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n unrar
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPPFLAGS="-I/usr/sfw/include -DANSICPP -DSOLARIS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D`uname -m`"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags}"
export STRIP=/usr/ccs/bin/strip

make -f makefile.unix -j$CPUS

%install
PREFIX=%{_prefix} \
LIBDIR=%{_libdir} \
BINDIR=%{_bindir} \
INSTALL=install \
make -f makefile.unix install DESTDIR=$RPM_BUILD_ROOT

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Converted to base spec
