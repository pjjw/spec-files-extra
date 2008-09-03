#
# spec file for package SFEgperf
#
# includes module(s): gperf
#
%include Solaris.inc

Name:                    SFEgperf
Summary:                 gperf - GNU perfect hash function generator
Version:                 3.0.3
Source:			         http://mirrors.kernel.org/gnu/gperf/gperf-%{version}.tar.gz
URL:                     http://www.gnu.org/software/gperf
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n gperf-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
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
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr(0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Wed Sep 3 2008 - <pradhap (at) gmail (dot) com>
- fixed link
* Thu Aug 30 2007 - laca@sun.com
- Create
