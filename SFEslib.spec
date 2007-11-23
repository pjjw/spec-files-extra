#
# spec file for package SFEslib 
#

%include Solaris.inc
Name:                    SFEslib
Summary:                 SLIB - Portable librart for Scheme programming language
URL:                     http://swissnet.ai.mit.edu/~jaffer/SLIB.html
Version:                 3a4
Source:                  http://swiss.csail.mit.edu/ftpdir/scm/slib%{version}.zip
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n slib
for i in *; do
  cp -f ${i} ${i}.orig
  sed -s "s,/usr/local/lib,%{_datadir},g" < ${i} > ${i}.orig
  sed -s "s,/usr/lib,%{_datadir},g" < ${i}.orig > ${i}
  sed -s "s,/usr/local,/usr,g" < ${i}.orig > ${i}
  rm -f ${i}.orig
done

%build
gzip -9nf slib.info

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/slib
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp *.scm *.init *.xyz *.txt grapheps.ps Makefile ${RPM_BUILD_ROOT}%{_datadir}/slib
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
install -m644 slib.info.gz ${RPM_BUILD_ROOT}%{_infodir}
make    prefix=${RPM_BUILD_ROOT}%{prefix}/ \
        mandir=${RPM_BUILD_ROOT}%{_mandir}/ \
        infodir=${RPM_BUILD_ROOT}%{_infodir}/ \
        pinstall

echo '#! /bin/sh'                        > ${RPM_BUILD_ROOT}%{_bindir}/slib
echo SCHEME_LIBRARY_PATH=%{_datadir}/slib/ >> ${RPM_BUILD_ROOT}%{_bindir}/slib
echo export SCHEME_LIBRARY_PATH         >> ${RPM_BUILD_ROOT}%{_bindir}/slib
echo VERSION=%{version}                 >> ${RPM_BUILD_ROOT}%{_bindir}/slib
echo "S48_VICINITY=\"%{_datadir}/scheme48\";export S48_VICINITY" >> ${RPM_BUILD_ROOT}%{_bindir}/slib
cat slib.sh                             >> ${RPM_BUILD_ROOT}%{_bindir}/slib
chmod +x ${RPM_BUILD_ROOT}%{_bindir}/slib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/slib
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*


%changelog
* Fri Nov 23 2007 - daymobrew@users.sourceforge.net
- Initial spec.
