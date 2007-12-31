#
# spec file for package SFExvid
#
# includes module(s): xvid
#
%include Solaris.inc

%define	src_ver 1.1.3
%define	src_name xvidcore
%define	src_url	http://downloads.xvid.org/downloads

Name:		SFExvid
Summary:	ISO MPEG-4 compliant video codec
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		xvid-01-solaris.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildConflicts: SFEyasm
%ifarch i386 amd64
BuildRequires: SFEnasm
%endif

%description
ISO MPEG-4 compliant video codec. You can play OpenDivX and DivX4 videos
with it, too.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-O4 -fPIC -DPIC -I/usr/X11/include -I/usr/openwin/include -D_LARGEFILE64_SOURCE -I/usr/gnu/include -mcpu=pentiumpro -mtune=pentiumpro -msse2 -mfpmath=sse"
export LDFLAGS=
export CC="/usr/gnu/bin/gcc"
export LD="/usr/gnu/bin/ld"
export CFLAGS="-O4"

cd build/generic
bash ./bootstrap.sh
# autotools changes -Wl,--version-script to -Wl,-M since
# it thinks we are using the Sun linker.  I do not know
# how to persuade autotools that we are actually using the
# gnu linker /usr/gnu/ld.  Hence the following sed hack.
mv configure configure.genned
sed -e 's/-Wl,-M,libxvidcore.ld/-Wl,--version-script,libxvidcore.ld/' configure.genned >configure
chmod ug+x configure
./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir}
gmake

%install
rm -rf $RPM_BUILD_ROOT
cd build/generic
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
(
   cd $RPM_BUILD_ROOT%{_libdir}
   ln -s libxvidcore.so.4.1 libxvidcore.so.4
   ln -s libxvidcore.so.4.1 libxvidcore.so
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon Dec 31 2007 - markwright@internode.on.net
- Use SFEgcc 4.2.2.  Add sed hack to change -Wl,-M back to
- -Wl,--version-script for /usr/gnu/bin/ld.
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
