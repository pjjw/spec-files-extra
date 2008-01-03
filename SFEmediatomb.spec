#
# spec file for package SFEmediatomb
#
# includes module(s): mediatomb
#
%include Solaris.inc

%define	src_name mediatomb
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/%{src_name}

Name:                SFEmediatomb
Summary:             UPnP AV MediaServer
Version:             0.10.0
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlibexif-devel
Requires: SUNWlibexif
BuildRequires: SFElibmagic-devel
Requires: SFElibmagic
BuildRequires: SFEid3lib-gnu-devel
Requires: SFEid3lib-gnu
BuildRequires: SUNWsqlite-devel
Requires: SUNWsqlite

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=/usr/gnu/bin:$PATH
export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/gnu/include"
export CFLAGS="-O4"
export CXXFLAGS="-O4"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/mediatomb

%changelog
* Tue Jul 17 2007 - dougs@truemail.co.th
- Initial spec
