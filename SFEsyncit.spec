#
# spec file for package SFEsyncit
#
# includes module(s): syncit
#

%define ocaml_dir /tmp/OCaml

%include Solaris.inc
Name:                    SFEsyncit
Summary:                 File-synchronization GUI tool
Version:                 0.1
Source:                  syncit-0.1.tar.bz2
SUNW_BaseDir:            %{_basedir}
URL: ???
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEunison
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%prep
%setup -q            -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export CPPFLAGS=""
export LDFLAGS=""
export MSGFMT="/usr/bin/msgfmt"

cd syncit*
aclocal $ACLOCAL_FLAGS
libtoolize --force
glib-gettextize --force --copy
intltoolize --force --automake
autoheader
automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix}

%install
cd syncit*
make -i install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Mon May 30 2006 - halton.huo@sun.com
- Initial spec file
