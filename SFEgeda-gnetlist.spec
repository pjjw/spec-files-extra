#
# spec file for package SFEgeda-gnetlist
#
# includes module(s): geda-gnetlist
#
%include Solaris.inc

%define	src_ver 20070526
%define	src_name geda-gnetlist
%define	src_url	ftp://ftp.geda.seul.org/pub/geda/devel/%{src_ver}

Name:		SFEgeda-gnetlist
Summary:	Utilites for gEDA project - netlist generator
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SFElibgeda-devel
Requires:	SFElibgeda
Requires:	SFEgeda-symbols

%description
Gnetlist generates netlists from schematics drawn with gschem (the
gEDA schematic editor). It supports many output formats including
native, Tango, Spice, Allegro, PCB, Verilog...

%package doc
Summary:                 %{summary} - Documentation
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

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal
autoconf -f
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gEDA
%{_mandir}

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
