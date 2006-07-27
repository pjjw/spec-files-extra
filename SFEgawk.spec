#
# spec file for package SFEgawk
#
# includes module(s): GNU awk
#
%include Solaris.inc

Name:                    SFEgawk
Summary:                 GNU awk - pattern scanning and processing filter
Version:                 3.1.5
Source:			 http://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%prep
%setup -q -n gawk-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Delete the awk->gawk symlink because awk is already on the system.
rm -f $RPM_BUILD_ROOT%{_bindir}/awk
mkdir -p $RPM_BUILD_ROOT%{_prefix}/gnu/bin
cd $RPM_BUILD_ROOT%{_prefix}/gnu/bin
ln -s ../../bin/gawk awk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}/gnu
%dir %attr (0755, root, bin) %{_prefix}/gnu/bin
%{_prefix}/gnu/bin/*
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/info
%dir %attr(0755, root, sys) %{_datadir}/awk
%{_datadir}/awk/*
%{_datadir}/info/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sun Jan 18 2006 - laca@sun.com
- rename to SFEgawk; update summary
- remove -share pkg
- make /usr/gnu/bin/awk a symlink to /usr/bin/gawk
* Thu Apr  6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Sun Dec  4 2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
