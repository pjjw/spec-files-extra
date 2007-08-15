#
# spec file for package SFEBillardGL
#
# includes module(s): BillardGL
#
%include Solaris.inc

%define	src_ver 1.75
%define	src_name BillardGL
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/billardgl

Name:		SFEBillardGL
Summary:	3D billard simulation using OpenGL
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		Billards-01-makefile.diff
Patch2:		Billards-02-sqrt.diff
Patch3:		Billards-03-std.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
3D billard simulation using OpenGL.

%prep
%setup -q -n %{src_name}-%version
find . -name \*.cpp -exec dos2unix {} {} \;
find . -name \*.h -exec dos2unix {} {} \;
find . -name Makefile -exec dos2unix {} {} \;
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd src

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"
export LD_OPTIONS="-L/usr/X11/lib -R/usr/X11/lib"
export PREFIX=%{_prefix}
export BINDIR=%{_bindir}
export DATADIR=%{_datadir}
export DOCDIR=%{_docdir}

make

%install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/BillardGL
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial spec
