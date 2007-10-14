#
# spec file for package SFEfreeglut.spec
#
# includes module(s): freeglut
#
%include Solaris.inc

%define src_name	freeglut
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/freeglut

Name:                   SFEfreeglut
Summary:                Free OpenGL Library
Version:                2.4.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEjam

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

bash ./autogen.sh
chmod 755 ./configure
#export CC=/usr/sfw/bin/gcc
#export CXX=/usr/sfw/bin/g++
#export CFLAGS="-O3 -fno-omit-frame-pointer -I/usr/X11/include"
#export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags -lX11 -L/usr/X11/lib -R/usr/X11/lib"
export LD_OPTIONS="-i"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_prefix}/X11/include	\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
	    --disable-warnings			\
            --enable-shared			\
	    --disable-static
jam

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_prefix}/X11/include

%changelog
* Sat Oct 13 2007 - laca@sun.com
- add /usr/X11 to CFLAGS and LDFLAGS to be able to build with FOX
* Tue Jun  5 2007 - dougs@truemail.co.th
- Added SFEjam as a build requirement
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
