#
# spec file for package SFEode.spec
#
# includes module(s): ode
#
%include Solaris.inc

%define src_name	ode
%define src_url		http://opende.sourceforge.net/snapshots

Name:                   SFEode
Summary:                high performance library for simulating rigid body dynamics
Version:                060223
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			ode-01-gcc-args.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

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


bash ./autogen.sh
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags -lX11"
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
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


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
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
