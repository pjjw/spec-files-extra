#
# spec file for package SFEqt3
#
# includes module(s): qt3
#

# NOTE: experimental 20080413 tomww - adjust paths for base-specs / patches if moved out of experimental
##TODO## discuss paths which could probably shared between gcc and sunstudio builds - consumers might get in troubles
##TODO## check consumers to use the new path layout /usr/qt/3 or /usr/qtgcc/3 
##TODO## check new path layout against what qt4 uses best

# The default install prefix is /usr/qt/3 to avoid conflicts 
# with other qt major versions
# Use <pkgbuild|pkgtool> --define '_basedir /path/to/dir'
# to define a different one.
# note: this is not heavily tested to produce good output paths

%{?!_basedir:%define gcc_basedir /usr/qtgcc/3}
%{?!_basedir:%define _basedir /usr/qt/3}

#helper stolen from Solaris.inc
%define cc_is_gcc %(test "x`basename $CC`" = xgcc && echo 1 || echo 0)

#if no user-defined basedir given, then gcc_basedir is defined and content is to be used
%if %{cc_is_gcc}
%{?gcc_basedir:%define _basedir %{gcc_basedir}}
%{?!gcc_subdir:%define qt_subdir /qtgcc/3}
%else
%{?!gcc_subdir:%define qt_subdir /qt/3}
%endif



%include Solaris.inc


##FIXME## check contents of arch_ldadd if they are needed/correct
%ifarch amd64 sparcv9
%include arch64.inc
%define arch_ldadd -Wl,-znolazyload -Wl,-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}
%define libdiradd /%{bld_arch}
%use qt364 = qt3-experimental.spec
%endif

%include base.inc
%define libdiradd 
%use qt3 = qt3-experimental.spec

# NOTE: special package-Name if CC=gcc (CXX=g++)
# NOTE: special default _basedir /usr/qtgcc/3 some lines above in this spec
%if %{cc_is_gcc}
Name:         SFEqt3gcc
%else
Name:         SFEqt3
%endif

Version:      %{qt3.version}
Summary:      Cross-platform development framework/toolkit (older version) 32- and 64-bit version
URL:          http://xml.apache.org/xalan-c/index.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name


%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%qt364.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%qt3.prep -d %name-%version/%{base_arch}




%build

%ifarch amd64 sparcv9
if [ "x`basename $CC`" != xgcc ]
then
	export PLATFORM=solaris-cc-64
else
	export PLATFORM=solaris-g++-64
fi
%qt364.build -d %name-%version/%_arch64
%endif

if [ "x`basename $CC`" != xgcc ]
then
	export PLATFORM=solaris-cc
else
	export PLATFORM=solaris-g++
fi
%qt3.build -d %name-%version/%{base_arch}




%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%qt364.install -d %name-%version/%_arch64
%endif

%qt3.install -d %name-%version/%{base_arch}

#only binaries for %{base_isa} should stay here (other bld_arch(es) place nothing here)
#base-isa is i86 or sparc(?)
[ -d $RPM_BUILD_ROOT%{_prefix}/bin/%{base_isa} ] || mkdir $RPM_BUILD_ROOT%{_prefix}/bin/%{base_isa}
for file in  `ls -1 $RPM_BUILD_ROOT%{_prefix}/bin/`
 do 
    [ -f $RPM_BUILD_ROOT%{_prefix}/bin/$file -a -x $RPM_BUILD_ROOT%{_prefix}/bin/$file ] || continue
    echo "preparing isaexec for file: $RPM_BUILD_ROOT%{_prefix}/bin/$file"
    mv $RPM_BUILD_ROOT%{_prefix}/bin/$file $RPM_BUILD_ROOT%{_prefix}/bin/%{base_isa}/
    # how many "/" below $RPM_BUILD_ROOT - add "../" to isaexec path depending how many "/" are in $file
    ISAEXECOFFSET=`echo %{_prefix}/bin/ | sed -e 's?/\{0,1\}\w*\(/\)?../?g' | sed -e 's?\(\w*$\)??'`
    ln -s ${ISAEXECOFFSET}../usr/lib/isaexec $RPM_BUILD_ROOT%{_prefix}/bin/$file
 done


# Create a compatibility doc link

##FIXME## to use correct paths
#(cd ${RPM_BUILD_ROOT}%{_docdir}/qt3
#  if [ -d doc ] 
#  then
#    mkdir doc
#    chmod 0755 doc
#    cd doc
#    ln -s ../../doc/qt3/html
#  fi
#)



%clean 
rm -rf $RPM_BUILD_ROOT

#%{_libdir}/*.so*

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{_arch64}/*
%{_bindir}/%{base_isa}/*
%hard %{_bindir}/assistant
%hard %{_bindir}/designer
%hard %{_bindir}/linguist
%hard %{_bindir}/lrelease
%hard %{_bindir}/lupdate
%hard %{_bindir}/moc
%hard %{_bindir}/qm2ts
%hard %{_bindir}/qmake
%hard %{_bindir}/qtconfig
%hard %{_bindir}/uic
%elseif
%{_bindir}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so.*
%{_libdir}/lib*.so
%dir %attr (0755, root, bin) %{_libdir}/plugins
%{_libdir}/plugins/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so.*
%{_libdir}/%{_arch64}/lib*.so
%{_libdir}/%{_arch64}/plugins/*
%dir %attr (0755, root, other)  %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%dir %attr (0755, root, other)  %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}%{qt_subdir}
%{_datadir}%{qt_subdir}/templates/*
%{_datadir}%{qt_subdir}/phrasebooks/*
%{_datadir}%{qt_subdir}/translations/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.prl
%{_libdir}/lib*.a
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.prl
%{_libdir}/%{_arch64}/lib*.a
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}%{qt_subdir}
%{_datadir}%{qt_subdir}/mkspecs/*

%files doc
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}%{qt_subdir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*


%changelog
* Sun Apr 13 2007    Thomas Wagner
- create 64-bit build as experimental, tested with virtualbox_OSE 64-bit from svn
