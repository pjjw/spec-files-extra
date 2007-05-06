#
# spec file for package SFEheroes.spec
#
# includes module(s): heroes
#
%include Solaris.inc

%define src_name	heroes
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/heroes
%define data_ver	1.5
%define st_ver		1.0
%define se_ver		1.0

Name:                   SFEheroes
Summary:                heroes game
Version:                0.21
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Source1:                %{src_url}/%{src_name}-data-%{data_ver}.tar.bz2
Source2:                %{src_url}/%{src_name}-hq-sound-tracks-%{st_ver}.tar.bz2
Source3:                %{src_url}/%{src_name}-sound-effects-%{se_ver}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl_mixer-devel
Requires: SFEsdl-mixer

%prep
%setup -q -b 1 -b 2 -b 3 -c -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


cd %{src_name}-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --infodir=%{_infodir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --with-sdl			\
	    --with-sdl-mixer		\
	    --without-mikmod		\
	    --without-gii		\
	    --without-ggi
make -j$CPUS 
cd ..

cd %{src_name}-data-%{data_ver}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --infodir=%{_infodir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 
cd ..

cd %{src_name}-hq-sound-tracks-%{st_ver}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --infodir=%{_infodir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 
cd ..

cd %{src_name}-sound-effects-%{se_ver}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --infodir=%{_infodir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 
cd ..

%install

rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
cd %{src_name}-data-%{data_ver}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
cd %{src_name}-hq-sound-tracks-%{st_ver}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
cd %{src_name}-sound-effects-%{se_ver}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir
rm -r ${RPM_BUILD_ROOT}%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}
%{_datadir}/info
%{_datadir}/heroes
%defattr (-, root, other)
%{_datadir}/locale


%changelog
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
