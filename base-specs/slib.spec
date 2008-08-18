#
# spec file for package slib
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

Name:           slib
Summary:        platform independent library for scheme
License:        distributable, see individual files for copyright
Group:          Development/Languages
Version:        3b1
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Source:         http://groups.csail.mit.edu/mac/ftpdir/scm/%{name}-%{version}.zip
URL:            http://people.csail.mit.edu/jaffer/SLIB
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
"SLIB" is a portable library for the programming language Scheme.
It provides a platform independent framework for using "packages" of
Scheme procedures and syntax.  As distributed, SLIB contains useful
packages for all Scheme implementations.  Its catalog can be
transparently extended to accomodate packages specific to a site,
implementation, user, or directory.

%prep
%setup -q -n %{name}
for i in *; do
  cp -f ${i} ${i}.orig
  sed "s,/usr/local/lib,%{_datadir},g" < ${i} > ${i}.orig
  sed "s,/usr/lib,%{_datadir},g" < ${i}.orig > ${i}
  sed "s,/usr/local,/usr,g" < ${i}.orig > ${i}
  rm -f ${i}.orig
done

%build
gzip -9nf slib.info

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/slib
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp *.scm *.init *.xyz *.txt grapheps.ps Makefile ${RPM_BUILD_ROOT}%{_datadir}/slib
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
install -m644 slib.info.gz ${RPM_BUILD_ROOT}%{_infodir}
make	prefix=${RPM_BUILD_ROOT}%{_prefix}/ \
	man1dir=${RPM_BUILD_ROOT}%{_mandir}/man1 \
	infodir=${RPM_BUILD_ROOT}%{_infodir}/ \
	pinstall

echo '#! /bin/sh'			 > ${RPM_BUILD_ROOT}%{_bindir}/slib
echo SCHEME_LIBRARY_PATH=%{_datadir}/slib/ >> ${RPM_BUILD_ROOT}%{_bindir}/slib
echo export SCHEME_LIBRARY_PATH		>> ${RPM_BUILD_ROOT}%{_bindir}/slib
echo VERSION=%{version}			>> ${RPM_BUILD_ROOT}%{_bindir}/slib
echo "S48_VICINITY=\"%{_datadir}/scheme48\";export S48_VICINITY" >> ${RPM_BUILD_ROOT}%{_bindir}/slib
cat slib.sh				>> ${RPM_BUILD_ROOT}%{_bindir}/slib
chmod +x ${RPM_BUILD_ROOT}%{_bindir}/slib

# make link for mklibcat
cd ${RPM_BUILD_ROOT}%{_datadir}/slib
ln -s mklibcat.scm mklibcat

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
# /sbin/install-info ${RPM_BUILD_ROOT}%{_infodir}/slib.info.gz %{_infodir}/dir

# This symlink is made as in the spec file of Robert J. Meier.
if [ -L /usr/share/guile/slib ]; then
  rm /usr/share/guile/slib
  ln -s %{_datadir}/slib /usr/share/guile/slib
fi

# Rebuild catalogs for as many implementations as possible.
export PATH=$PATH:/usr/bin
echo PATH=${PATH}
cd %{_datadir}/slib/
make catalogs

# %postun
# if [ $1 = 0 ]; then
#   /sbin/install-info --delete %{_infodir}/slib.info.gz %{_infodir}/dir
# fi

%preun
cd %{_datadir}/slib/
rm -f slib.image

%files
%defattr(-, root, root)
%{_bindir}/slib
%dir %{_datadir}/slib
%{_datadir}/slib/*.scm
%{_datadir}/slib/*.init
%{_datadir}/slib/cie1931.xyz
%{_datadir}/slib/cie1964.xyz
%{_datadir}/slib/nbs-iscc.txt
%{_datadir}/slib/saturate.txt
%{_datadir}/slib/resenecolours.txt
%{_datadir}/slib/grapheps.ps
%{_datadir}/slib/Makefile
%{_infodir}/slib.info.gz
# %{_mandir}/man1/slib.1.gz
%doc ANNOUNCE README COPYING FAQ ChangeLog

%changelog
* Mon Aug 18 2008 - nonsea@users.sourceforge.net
- Fix URL and Source
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- initial version
