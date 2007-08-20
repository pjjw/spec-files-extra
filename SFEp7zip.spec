#
# spec file for package SFEp7zip
#
# includes module(s): p7zip
#
%include Solaris.inc

Name:                    SFEp7zip
Summary:                 7-Zip file archiver with a high compression ratio
Version:                 4.51
Source:			 http://umn.dl.sourceforge.net/sourceforge/p7zip/p7zip_4.51_src_all.tar.bz2
Patch1:                  p7zip-01-makefile.diff
URL:                     http://www.7-zip.org/download.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n p7zip_%{version}
%patch1 -p1
cp makefile.solaris_x86 makefile.machine

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch x86
ENDIAN_MACRO="-DLITTLE_ENDIAN"
%else
%ifarch sparc	    		
ENDIAN_MACRO="-DBIG_ENDIAN"
%endif
%endif

make -j$CPUS all MY_CXX="$CXX" CXX_OPTFLAGS="%cxx_optflags" MY_CC="$CC" CC_OPTFLAGS="%optflags" ENDIAN_MACRO="$ENDIAN_MACRO"

%install
chmod -R u+w $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install DEST_HOME=$RPM_BUILD_ROOT%{_prefix} DEST_MAN=$RPM_BUILD_ROOT%{_mandir}
perl -pi -e "s,$RPM_BUILD_ROOT,,g" $RPM_BUILD_ROOT%{_bindir}/7za

%clean
chmod -R u+w $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/p7zip
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/p7zip
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sun Aug 20 2007 - laca@sun.com
- Create
