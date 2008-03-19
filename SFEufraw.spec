#
# spec file for package SFEufraw
#
# includes module(s): ufraw
#
%include Solaris.inc

Name:                    SFEufraw
Summary:                 Ufraw - Raw Photo Converter
Version:                 0.12.1
Source:                  %{sf_download}/ufraw/ufraw-%{version}.tar.gz
URL:                     http://ufraw.sourceforge.net/
Patch1:			 ufraw-01-ctime_r-fix.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlcms-devel
BuildRequires: SUNWgnome-libs-devel
Requires: SUNWlcms
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-img-editor
Requires: SUNWjpg
Requires: SUNWTiff
Requires: SUNWmlib
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWlibexif
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-img-editor-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWmlibh
BuildRequires: SUNWlibm
BuildRequires: SUNWlibexif-devel
# dos2unix:
BuildRequires: SUNWesu
# pod2man:
BuildRequires: SUNWperl584usr

%prep
%setup -q -n ufraw-%version
%patch1 -p1
touch NEWS
touch AUTHORS
for f in *.[ch]; do dos2unix -ascii $f $f; done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -DSOLARIS"
export LDFLAGS="%_ldflags"
export POD2MAN=/usr/perl5/bin/pod2man
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLASG="%cxx_optflags"
autoconf
./configure --prefix=%{_prefix} --enable-extras --with-libexif \
	--mandir=%{_mandir} --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --includedir=%{_includedir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make BASENAME=${RPM_BUILD_ROOT}%{_prefix}	\
     MANDIR=${RPM_BUILD_ROOT}%{_mandir} DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
/usr/lib/gimp/2.0/plug-ins/*


%changelog
* Wed Oct 17 2007 - laca@sun.com
- bump to 0.12.1
* Wed Jul  5 2006 - laca@sun.com
- bump to 0.8.1
- rename to SFEufraw
- move to /usr
- update file attributes
* Fri May  5 2006 - damien.carbery@sun.com
- Bump to 0.8.
* Thu Apr  6 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Thu Mar 30 2006 - damien.carbery@sun.com
- Change Source URL to working server and add project URL.
* Fri Mar 17 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
