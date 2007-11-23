#
# spec file for package SFEurxvt
#

#TODO# urxvt does not set terminal-size. have to use: stty rows 50; stty columns 132; export LINES=50 COLUMNS=132
#TODO# cleanup environment setting CFLAGS/CXXFLAGS/LDFLAGS...
#TODO# solve build errors with --enable-perl 
#TODO# something like infocmp -C rxvt-unicode >> /etc/termcap as postinstall script (safely) - "screen" needs this
#TODO# put nice descrition of features into %description
#TODO# really need fix the terminfo entries, "tic" issues warnings....
#TODO# check libafterimage - if usefull, add

#   IMPORTANT:
#   compile with:   CC=/usr/sfw/bin/gcc CXX=/usr/sfw/bin/g++ pkgtool --interactive build SFEurxvt.spec
#
#   tested with: SFEgcc (older version gcc 4.0.0) and /usr/sfw/bin/gcc
#
#   NOT working with: sunstudio 12,  SFEgcc 4.2 (incl. gnu ld)
#       if you do not specify the CC/CXX before running pkgtool (see above) you might get 
#       gnu 4.x.x or sunstudio compilers...
#

%include Solaris.inc

%include base.inc


Name:                    SFEurxvt
Summary:                 urxvt - X Terminal Client (+multiscreen Server) with unicode support, derived from rxvt
URL:                     http://software.schmorp.de
Version:                 8.4
Source:                  http://dist.schmorp.de/rxvt-unicode/rxvt-unicode-%{version}.tar.bz2
Patch10:		 urxvt-10-terminfo_enacs.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc


%description
urxvt is a Multiscreenserver and Client for Terminal emulation. Supports Unicode
charsets and has tons of nice features. With "compiz" you can enable traparent 
backgrounds (unmodified or shaded background inside the Terminal window)


%prep
%setup -q -n rxvt-unicode-%{version}
%patch10 -p1


%build
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-i -L/usr/X11/lib -R/usr/X11/lib -L/usr/openwin/lib -R/usr/openwin/lib"
export LD=/opt/jdsbld/bin/ld-wrapper
#export CFLAGS="%optflags -D_XPG5 -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"
#export CXXFLAGS="%cxx_optflags -D_XPG5 -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"
export CFLAGS="%optflags -L/usr/X11/lib -R/usr/X11/lib -lX11 -lXext -lXrender"
export CXXFLAGS="%cxx_optflags"



# Note: Use CC=/usr/sfw/bin/gcc CXX=/usr/sfw/bin/g++

./configure \
            --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
 	    --enable-shared \
 	    --disable-static \
            --enable-transparency \
            --enable-24bits \
            --enable-xft  \
            --disable-perl \
            --enable-xgetdefault \
            --enable-mousewheel \
            --disable-menubar \
            --enable-ttygid \
            --enable-half-shadow \
            --enable-smart-resize \
            --enable-256-color \
            --enable-24bit \
            --enable-unicode3\
            --enable-combining\
            --enable-xft       \
            --enable-font-styles\
            --enable-afterimage\
            --enable-transparency  \
            --enable-fading    \
            --enable-tinting    \
            --enable-rxvt-scroll\
            --enable-next-scroll \
            --enable-xterm-scroll \
            --enable-plain-scroll \
            --enable-xim           \
            --enable-xpm-background \
            --enable-fallback \
            --enable-resources \
            --with-save-lines=2000 \
            --enable-linespace \
            --enable-iso14755    \
            --enable-frills       \
            --enable-keepscrolling \
            --enable-selectionscrolling \
            --enable-mousewheel  \
            --enable-slipwheeling \
            --enable-smart-resize\
            --enable-text-blink   \
            --enable-pointer-blank \
            --enable-utmp \
            --enable-wtmp  \
            --enable-lastlog\
            --with-codesets=all
         


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p "$RPM_BUILD_ROOT/%{_datadir}/terminfo/"
TERMINFO=$RPM_BUILD_ROOT/%{_datadir}/terminfo/  tic -v doc/etc/rxvt-unicode.terminfo

%clean
rm -rf $RPM_BUILD_ROOT


#TODO# postinstall with infocmp -C rxvt-unicode >> /etc/termcap if !grep "^rxvt-unicode" /etc/termcap
#TODO# postinstall display note to user to really read the README.FAQ with tons of usefull hints


%files
%defattr(-, root, bin)
%doc README* ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/terminfo/r/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*



%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}/locale
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Fri Nov 23 2007  - Thomas Wagner
- refined, first version of terminfo/termcap
- open issues see TODO - any ideas?
* Sat Jul 14 2007  - Thomas Wagner
- Initial spec
