#
# spec file for package SFEmono
#
# includes module(s): mono
#

%include Solaris.inc

Name:         SFEmono
License:      Other
Group:        System/Libraries
Version:      1.1.16.1
Summary:      mono - .NET framework
Source:       http://go-mono.com/sources/mono/mono-%{version}.tar.gz
URL:          http://www.mono-project.com/Main_Page
Patch1:       mono-01-solaris.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs
Requires:     %name-root
Requires: SUNWbash
Requires: SUNWgccruntime

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n mono-%version
%patch1 -p1 -b .patch01

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# doesn't currently build with Forte
export CC=/usr/sfw/bin/gcc
export CFLAGS="-fPIC -DPIC -Xlinker -i -fno-omit-frame-pointers"

#export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
                --bindir=%{_prefix}/mono/bin \
		--mandir=%{_mandir} \
		--libdir=%{_libdir} \
		--libexecdir=%{_libexecdir} \
		--sysconfdir=%{_sysconfdir} \
		-with-tls=pthread
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lib*.a
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_bindir}/jay $RPM_BUILD_ROOT%{_prefix}/mono/bin
rmdir $RPM_BUILD_ROOT%{_bindir}

mv $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_mandir}/man1mono
cd $RPM_BUILD_ROOT%{_mandir}/man1mono
for fn in *; do
    f=`basename $fn .1`
    sed -e 's/^\.TH \([^ ]*\) 1/.TH \1 1MONO/' $f.1 > $f.1mono
    rm -f $f.1
done
ln -s mcs.1mono gmcs.1mono

mv $RPM_BUILD_ROOT%{_mandir}/man5 $RPM_BUILD_ROOT%{_mandir}/man5mono
cd $RPM_BUILD_ROOT%{_mandir}/man5mono
for fn in *; do
    f=`basename $fn .5`
    sed -e 's/^\.TH \([^ ]*\) 5/.TH \1 5MONO/' $f.5 > $f.5mono
    rm -f $f.5
done

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_prefix}/mono/bin
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, sys) %dir %{_datadir}/jay
%{_datadir}/jay/*
%{_datadir}/mono
%{_datadir}/libgc-mono
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1mono
%{_mandir}/man1mono/*
%dir %attr(0755, root, bin) %{_mandir}/man5mono
%{_mandir}/man5mono/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}/mono

%files devel
%defattr (-, root, bin)
%{_includedir}/mono
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Jul 15 2006 - laca@sun.com
- rename to SFEmono
- bump to 1.1.16.1
- include Solaris.inc
- force using gcc
- move bin files to /usr/mono/bin
* Wed Jul 12 2006 - jedy.wang@sun.com
- Initial spec
