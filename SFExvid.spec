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

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export CC=gcc
export CFLAGS="-O4"

cd build/generic
bash ./bootstrap.sh
./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir}
make

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
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
