#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEe2fsprogs
License:             GPL
Summary:             Ext2 Filesystems Utilities
Version:             1.40.5
URL:                 http://e2fsprogs.sourceforge.net/
Source:              http://nchc.dl.sourceforge.net/sourceforge/e2fsprogs/e2fsprogs-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n e2fsprogs-%version

if [ "x`basename $CC`" != xgcc ]
then
        %error This spec file requires Gcc, set the CC and CXX env variables
fi


%build

export CFLAGS="%optflags -I%{gnu_inc} -DINSTALLPREFIX=\\\"%{_prefix}\\\""
export LDFLAGS="%_ldflags %{gnu_lib_path} -liconv -lintl"
export PATH=/usr/bin:${PATH}

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes \
            --enable-static=no  \
            --with-pic

cp config/asm_types.h .

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Copy files for the devel package
cp lib/libext2fs.a $RPM_BUILD_ROOT%{_libdir}
cp lib/libcom_err.a $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/ext2fs
mkdir -p $RPM_BUILD_ROOT%{_includedir}/et

cp lib/ext2fs/bitops.h $RPM_BUILD_ROOT%{_includedir}/ext2fs
cp lib/ext2fs/ext2_err.h $RPM_BUILD_ROOT%{_includedir}/ext2fs
cp lib/ext2fs/ext2_io.h $RPM_BUILD_ROOT%{_includedir}/ext2fs
cp lib/ext2fs/ext2fs.h $RPM_BUILD_ROOT%{_includedir}/ext2fs
cp lib/ext2fs/ext2_fs.h $RPM_BUILD_ROOT%{_includedir}/ext2fs
cp lib/ext2fs/ext2_types.h $RPM_BUILD_ROOT%{_includedir}/ext2fs
cp lib/ext2fs/ext3_extents.h $RPM_BUILD_ROOT%{_includedir}/ext2fs

# Remove stuff that conflict with Solaris native utilities
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}
rm $RPM_BUILD_ROOT%{_sbindir}/fsck

# Create dirs and symlinks to match with the OpenSolaris scheme of things
# TODO: Man pages do not match. It requires creating additional patched man pages.
#
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/ext2fs
(cd $RPM_BUILD_ROOT%{_libdir}/fs
    ln -s ext2fs ext3fs)

rm $RPM_BUILD_ROOT%{_sbindir}/fsck.ext2
rm $RPM_BUILD_ROOT%{_sbindir}/fsck.ext3
rm $RPM_BUILD_ROOT%{_sbindir}/mkfs.ext2
rm $RPM_BUILD_ROOT%{_sbindir}/mkfs.ext3

(cd $RPM_BUILD_ROOT%{_libdir}/fs/ext2fs
    ln -s ../../../../%{_sbindir}badblocks
    ln -s ../../../../%{_sbindir}blkid
    ln -s ../../../../%{_sbindir}debugfs
    ln -s debugfs fsdb
    ln -s ../../../../%{_sbindir}dumpe2fs dump
    ln -s ../../../../%{_sbindir}e2fsck fsck
    ln -s ../../../../%{_sbindir}e2image
    ln -s e2image fsimage
    ln -s ../../../../%{_sbindir}e2label labelit
    ln -s ../../../../%{_sbindir}filefrag
    ln -s ../../../../%{_sbindir}findfs
    ln -s ../../../../%{_sbindir}logsave
    ln -s ../../../../%{_sbindir}mke2fs mkfs
    ln -s ../../../../%{_sbindir}mklost+found
    ln -s ../../../../%{_sbindir}resize2fs resize
    ln -s ../../../../%{_sbindir}tune2fs tunefs
    ln -s ../../../../%{_sbindir}uuid)

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/ext2fs
%{_libdir}/fs/ext2fs/*
%{_libdir}/fs/ext3fs
%attr (0755, root, bin) %{_libdir}/e2initrd_helper

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.a

%changelog
* Sat Feb 02 2008 - moinak.ghosh@sun.com
- Initial spec.
