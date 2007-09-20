
%define PN rsnapshot
%define PV 1.3.0
%define P  %{PN}-%{PV}
%define DESCRIPTION A filesystem backup utility based on rsync.
%define SRC_URI http://www.rsnapshot.org/downloads/%{P}.tar.gz
%define HOMEPAGE http://www.rsnapshot.org
%define CATEGORY app,backup
%define PROVIDES %{PN}-%{PV}

%include Solaris.inc
Name:                    SFE%{PN}
Summary:                 %{PN} - %{DESCRIPTION}
Group:					 %{CATEGORY}
Version:                 %{PV}
Source:                  %{SRC_URI}
URL:			 		 %{HOMEPAGE}		 
SUNW_BaseDir:            %{_basedir}
SUNW_Category:           SFE,application,%{CATEGORY}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc
Requires:				SUNWrsync
Requires:				SUNWsshu


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
%setup -q -n %{PN}-%{PV}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --libexecdir=%{_libexecdir} \
			--sysconfdir=%{_sysconfdir}

#Inline patch for pod2man location
sed -i 's:/usr/bin/pod2man:/usr/perl5/bin/pod2man:' Makefile

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*


%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*


%changelog
* Mon Sep 20 2007 - flistellox@gmail.com
- Initial Specs
