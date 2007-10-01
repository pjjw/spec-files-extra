#
# spec file for package SFEzfs-auto-backup.spec^
#
# includes module(s): zfs-auto-backup
#
%include Solaris.inc

%include base.inc

%define src_name        zfs-auto-backup
%define src_url         http://mediacast.sun.com/share/timf/


Name:                   SFEzfs-auto-backup
Summary:                zfs-auto-backup service. Plugin configured storage and full/incremental backup of flagged zfs-filesystems starts (recursively)
Version:                0.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Url:			http://blogs.sun.com/timf/entry/zfs_automatic_backup_0_1
SUNW_BaseDir:           /
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -n %{src_name}-%{version}

%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/svc/method
cp -p lib/svc/method/svc-zfs-auto-backup $RPM_BUILD_ROOT/lib/svc/method
mkdir -p $RPM_BUILD_ROOT/usr/lib
cp -p usr/lib/zfs-auto-backup.ksh $RPM_BUILD_ROOT/usr/lib
cp -p usr/lib/zfs-auto-backupd.py $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps
cp -p zfs-man.png $RPM_BUILD_ROOT/usr/share/pixmaps



mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/system/filesystem/zfs/
cp zfs-auto-backup.xml ${RPM_BUILD_ROOT}/var/svc/manifest/system/filesystem/zfs/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%post -n SFEzfs-auto-backup-root

if [ -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ]; then
       /usr/sbin/svccfg import /var/svc/manifest/system/filesystem/zfs/zfs-auto-backup.xml
    fi
fi

echo "Remember to configure the Name/Label of your pluggable Backupmedia:" 1>&2
echo "svccfg -s svc:/system/filesystem/zfs/auto-backup:default setprop zfs/volume = astring: \"MYVOL\"" 1>&2
echo "svcadm refresh svc:/system/filesystem/zfs/auto-backup:default" 1>&2

exit 0

%preun -n SFEzfs-auto-backup-root
if [  -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ]; then
       if [ `svcs  -H -o STATE svc:/system/filesystem/zfs/auto-backup:default` != "disabled" ]; then
           svcadm disable svc:/system/filesystem/zfs/auto-backup:default
       fi
    fi
fi


%postun -n SFEzfs-auto-backup-root

if [ -f /lib/svc/share/smf_include.sh ] ; then
    . /lib/svc/share/smf_include.sh
    smf_present
    if [ $? -eq 0 ] ; then
       /usr/sbin/svccfg export svc:/system/filesystem/zfs/auto-backup:default > /dev/null 2>&1
       if [ $? -eq 0 ] ; then
           /usr/sbin/svccfg delete -f svc:/system/filesystem/zfs/auto-backup:default
       fi
    fi
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}/
%{_libdir}/zfs*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) /lib
/lib/svc/method/*



%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_localstatedir}
%defattr (0755, root, sys)
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/system/filesystem/zfs/zfs-auto-backup.xml
   


%changelog
* Tue Oct 02 2007 - Thomas Wagner
- Initial version
- corrected files-section and pkgremove-scripts
