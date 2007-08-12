#
# spec file for package SFElibraptor
#
# includes module(s): libraptor
#
%include Solaris.inc

%define	src_ver 1.4.15
%define	src_name raptor
%define	src_url	http://download.librdf.org/source

Name:		SFElibraptor
Summary:	Raptor RDF Parser Library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires: SFEcurl

%description
Raptor is a free software / Open Source C library that provides a set of
parsers and serializers that generate Resource Description Framework (RDF)
triples by parsing syntaxes or serialize the triples into a syntax.
The supported parsing syntaxes are RDF/XML, N-Triples, Turtle, RSS tag soup
including Atom 1.0 and 0.3, GRDDL for XHTML and XML. The serializing syntaxes
are RDF/XML (regular, and abbreviated), N-Triples, RSS 1.0, Atom 1.0
and Adobe XMP.

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
