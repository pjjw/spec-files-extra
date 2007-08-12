#
# spec file for package SFElibrasqal
#
# includes module(s): librasqal
#
%include Solaris.inc

%define	src_ver 0.9.14
%define	src_name rasqal
%define	src_url	http://download.librdf.org/source

Name:		SFElibrasqal
Summary:	Rasqal RDF Query Library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SFElibraptor-devel
Requires:	SFElibraptor

%description
Rasqal is a free software / Open Source C library that handles
Resource Description Framework (RDF) query syntaxes, query construction
and query execution returning result bindings. The supported query
languages are SPARQL and RDQL.

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_prefix}
%include default-depend.inc
Requires: %name

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

glib-gettextize -f
libtoolize --copy --force
aclocal
autoconf -f
autoheader
automake -a -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
