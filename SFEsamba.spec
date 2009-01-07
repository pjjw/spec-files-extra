#
# spec file for package SFEsamba
#
# works: snv105 / pkgbuild 1.3.91 / Sun Ceres C 5.10 SunOS_i386 2008/10/22
# works: snv104 / pkgbuild 1.2.0 (old!) / Sun C 5.9 SunOS_i386 Patch 124868-02 2007/11/27

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/sfw/bin/g++
%include base.inc

#avoid clush with /usr/bin/profiles of SUNWcsu Solaris package
%include usr-gnu.inc

%define src_name samba

Name:                    SFEsamba
Summary:                 samba - CIFS Server and Domain Controller
URL:                     http://samba.org/
Version:                 3.2.7
Copyright:               GPL
Url:                     http://www.samba.org
Source:                  http://download.samba.org/samba/ftp/stable/samba-%{version}.tar.gz
Source2:		samba.xml
Patch2:                  samba-02-eliminate-selftest-bcs-buildroot-not-recognized.diff
Patch3:                  samba-03-Makefile-add-DESTDIR_RPM_BUILD_ROOT.diff
Patch4:                  samba-04-ext-sources-manifest-gnu-names.diff
Patch5:                  samba-05-smb.conf.default-add-machine-script-useradd.diff


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqires:
BuildRequires: SUNWbash
#TODO: Reqires:
Requires: SUNWbash

%include default-depend.inc

%package swat
Summary:                 %{summary} - swat management web frontend
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package doc
Summary:                 %{summary} - documentation and manpages
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name



%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%description


%prep
%setup -q -n samba-%version
%patch2 -p1

perl -w -pi.bak -e "s,^SHELL=/bin/sh,SHELL=/usr/bin/bash," source/Makefile.in source/Makefile
perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," `find source -type f -exec grep -q "^#\!.*/bin/sh" {} \; -print`

#samba manifest
cp -p %{SOURCE2} sambagnu.xml
%patch4 -p0

#solaris useradd smb.conf.default
%patch5 -p1

%build

export SHELL=/usr/bin/bash

export CC="/usr/sfw/bin/gcc"
export CXX="/usr/sfw/bin/g++"

#export CFLAGS="%optflags -DNO_PROTO_H"
export CFLAGS="%optflags -L /usr/gnu/lib/samba -R /usr/gnu/lib/samba"
export CXXFLAGS="%cxx_optflags -L /usr/gnu/lib/samba -R /usr/gnu/lib/samba"
export LDFLAGS="%_ldflags -L /usr/gnu/lib/samba -R /usr/gnu/lib/samba"


cd source
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --bindir=%{_bindir}         \
            --sbindir=%{_sbindir}         \
            --libdir=%{_libdir}/samba         \
            --libexecdir=%{_libexecdir}/samba \
            --sysconfdir=%{_sysconfdir}/samba \
	    --with-configdir=%{_sysconfdir}/samba \
	    --with-privatedir=%{_sysconfdir}/samba/private \
	    --sharedstatedir=%{_localstatedir}/samba \
	    --localstatedir=%{_localstatedir}/samba \
	    --datadir=%{_datadir} \
	    --with-swatdir=%{_datadir}/samba/swat \
            --disable-static        \
            SHELL=/usr/bin/bash     \
            LDFLAGS="-L /usr/gnu/lib/samba -R /usr/gnu/lib/samba "

#            LDFLAGS=${LDFLAGS}      \
#            CFLAGS=${CFLAGS}        \
#            CXXFLAGS=${CXXFLAGS}

  # --datarootdir=DIR      read-only arch.-independent data root [PREFIX/share]
  #--localedir=DIR        locale-dependent data [DATAROOTDIR/locale]

%patch3 -p2


#no parallel build please :-)
make

%install
rm -rf $RPM_BUILD_ROOT
cd source
SHELL=/usr/bin/bash make install DESTDIR=$RPM_BUILD_ROOT
  	
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/samba/private
cp -p ../examples/smb.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/samba/

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp ../sambagnu.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc COPYING MAINTAINERS README WHATSNEW.txt
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/smbd
%{_sbindir}/nmbd
%{_sbindir}/winbindd
#swat see below
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
#for doc section from above
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
#%dir %attr (0755, root, other) %{_docdir}/%{src_name}

#note manpage(s) swat included
%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files swat
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/swat
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/%{src_name}
%dir %attr (0755, root, bin) %{_datadir}/%{src_name}/swat
%{_datadir}/%{src_name}/swat/*


%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/sambagnu.xml



%changelog
* Wed Jan  7 2009 - Thomas Wagner
- remove %post, %preun, %postun
- bump to version 3.2.7 to solve CVE-2009-0022 and CVE-2008-4314
- clean %doc, add mkdir %{_docdir} for compatibility to older pkgbuild/pkgtool
* Mon Oct 13 2008 - Thomas Wagner
- typo at mkdir for samba log
* Fri Oct 03 2008 - Thomas Wagner
- derive new SMF instance from samba.xml and add postinstall for import
* Sat Sep 13 2008 - Thomas Wagner
- Initial spec - derived from LSB/lsb-samba.spec


