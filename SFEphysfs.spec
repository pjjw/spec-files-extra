#
# spec file for package SFEphysfs.spec
#
# includes module(s): physfs
#
%include Solaris.inc

%define src_name	physfs
%define src_url		http://icculus.org/physfs/downloads

Name:                   SFEphysfs
Summary:                Yet another assembler
Version:                1.1.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			physfs-01-alloca.diff
Patch2:                 physfs-02-inline.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEcmake

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

echo $CC | grep gcc 2>&1 > /dev/null
if [ $? -ne 0 ]
then
	CFLAGS="$CFLAGS -xc99"
fi
cmake .
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
find . -name libphysfs.so\* | cpio -pdm $RPM_BUILD_ROOT%{_libdir}
cp physfs.h $RPM_BUILD_ROOT%{_includedir}
cp test_physfs $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Changes to compile inline functions (C99) with Sun Studio
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
