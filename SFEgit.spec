#
# spec file for package : SFEgit
#
# includes module(s): git
#
# %description
# This is a stupid (but extremely fast) directory content manager.  It
# doesn't do a whole lot, but what it _does_ do is track directory
# contents efficiently. It is intended to be the base of an efficient,
# distributed source code management system. This package includes
# rudimentary tools that can be used as a SCM, but you should look
# elsewhere for tools for ordinary humans layered on top of this.
#
%include Solaris.inc

Name:                SFEgit
Summary:             GIT - the stupid content tracker
Version:             1.4.4
Source:              http://kernel.org/pub/software/scm/git/git-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEcurl 
BuildRequires: SFEcurl-devel
Requires: SFEcurl
Requires: SUNWzlib
Requires: SUNWsshu
Requires: SUNWopenssl-libraries
Requires: SUNWlexpt
Requires: SFEdiffutils
Requires: SUNWTk
%define perl_version 5.8.4
Requires: SUNWperl584core
Requires: SUNWPython
BuildRequires: SFEasciidoc
BuildRequires: SFExmlto

%prep
%setup -q -n git-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-O4"
export LDFLAGS="%_ldflags"
make configure
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --with-perl=/usr/perl5/bin/perl
make -j$CPUS all doc

# fix path to wish (tk shell)
perl -pi -e 's,exec wish ,exec /usr/sfw/bin/wish8.3,' gitk

# fix perl lib dir:
for f in "
    git-archimport
    git-cvsexportcommit
    git-cvsimport
    git-cvsserver
    git-relink
    git-rerere
    git-send-email
    git-shortlog
    git-svn
    git-svnimport"; do
  perl -pi -e 's,"/usr/lib/site_perl","/usr/perl5/vendor_perl/%{perl_version}",' $f
done

%install
rm -rf $RPM_BUILD_ROOT

make install install-doc DESTDIR=$RPM_BUILD_ROOT INSTALL=install

# move perl stuff to vendor_perl
mkdir -p $RPM_BUILD_ROOT/usr/perl5/vendor_perl/%{perl_version}
mv $RPM_BUILD_ROOT%{_libdir}/site_perl/*.pm $RPM_BUILD_ROOT/usr/perl5/vendor_perl/%{perl_version}

# remove unwanted stuff like .packlist and perllocal.pod
rm -r $RPM_BUILD_ROOT%{_libdir}/site_perl
rm $RPM_BUILD_ROOT%{_libdir}/*-solaris-*/perllocal.pod
rmdir $RPM_BUILD_ROOT%{_libdir}/*-solaris-*
rmdir $RPM_BUILD_ROOT%{_libdir}

# move man3 pages to the right place
mv $RPM_BUILD_ROOT%{_prefix}/man/man3 $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/git*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/git-core
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*
%dir %attr (0755, root, bin) %{_prefix}/perl5
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*

%changelog
* Tue Feb 13 2007 - laca@sun.com
- finish Erwann's spec
* Tue Feb 13 2007 - erwann@sun.com
- Initial spec
