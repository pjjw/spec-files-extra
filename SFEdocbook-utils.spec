#
# spec file for package SFEdocbook-utils
#
# includes module(s): docbook-utils
#
%include Solaris.inc

%define	src_name docbook-utils
%define	src_url	ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES

Name:                SFEdocbook-utils
Summary:             Shell scripts to manage DocBook documents.
Version:             0.6.14
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     docbook-utils-01-sh.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWopenjade
Requires: SFEperl-SGMLpm

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

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT docdir=%{_docdir} mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/sgml
%{_mandir}

%changelog
* Tue Sep  4 2007 - dougs@truemail.co.th
- Fixed typo
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
