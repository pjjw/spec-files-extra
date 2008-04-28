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
Version:             1.5.4.2
URL:                 http://git.or.cz/
Source:              http://www.kernel.org/pub/software/scm/git/git-%{version}.tar.bz2
Patch1:              git-01-solaris-shell.diff
Patch2:              git-02-fixshell.diff
Patch3:              git-03-tr.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWsshu
Requires: SUNWopenssl-libraries
Requires: SUNWlexpt
Requires: SUNWcurl
Requires: SUNWperl584core
Requires: SUNWPython
Requires: SUNWbash
Requires: SUNWlexpt
%if %(pkginfo -q SUNWgnu-diffutils && echo 1 || echo 0)
Requires: SUNWgnu-diffutils
%else
Requires: SFEdiffutils
%endif
Requires: SUNWTk
%define perl_version 5.8.4
BuildRequires: SFEasciidoc
BuildRequires: SFExmlto

%prep
%setup -q -n git-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-O4"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"
export PATH=$PATH:%{_builddir}/git-%version
export NO_MSGFMT=1
make configure
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --with-perl=/usr/perl5/bin/perl
make all doc

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/git*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gitk
%dir %{_datadir}/git-core
%dir %{_datadir}/git-core/templates
%{_datadir}/git-core/templates/branches
%{_datadir}/git-core/templates/description
%{_datadir}/git-core/templates/info
%dir %{_datadir}/git-core/templates/hooks
%defattr (0644, root, bin)
%{_datadir}/git-core/templates/hooks/*
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_datadir}/git-gui
%dir %attr (0755, root, bin) %{_datadir}/git-gui/lib
%{_datadir}/git-gui/lib/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*
%dir %attr (0755, root, bin) %{_prefix}/perl5
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*

%changelog
* Wed Apr 23 2008 - trisk@acm.jhu.edu
- Add patch3 to fix bisect problem with non-GNU tr
* Thu Mar 13 2008 - nonsea@users.sourceforge.net
- s/SFEcurl/SUNWcurl
* Fri feb 22 2008 - brian.cameron@sun.com
- Add patch git-02-fixshell.diff to fix a build problem caused
  by a script that requires bash.
* Thu Feb 21 2008 - nonsea@users.sourceforge.net
- Bump to 1.5.4.2
* Thu Dec 06 2007 - brian.cameron@sun.com
- Bump to 1.5.3.7.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Change LDFLAGS to work for gcc.
* Tue Sep 18 2007 - brian.cameron@sun.com
- Bump to 1.5.3.
* Thu Jul 05 2007 - alberto.ruiz@sun.com
- fixing hook templates permisions
* Tue Jul 03 2007 - alberto.ruiz@sun.com
- changing version to 1.5.2.2 and declaring new files
* Fri Jun 22 2007 - laca@sun.com
- make it build with either SUNWgnu-diffutils or SFEdiffutils
* Tue Feb 13 2007 - laca@sun.com
- finish Erwann's spec
* Tue Feb 13 2007 - erwann@sun.com
- Initial spec
