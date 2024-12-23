%define         srcname        fvwm3
%define         cfgname        %{name}-config-mageia
%define         fvwmconfdir    %{_sysconfdir}/fvwm3
%define         docname        %{name}-doc

Name:           fvwm3
Version:        1.1.1
Release:        %mkrel 2
Summary:        FVWM version 3, the successor to fvwm2 
License:        GPLv2+
Group:          Graphical desktop/Other

URL:            https://www.fvwm.org/
Source0:        https://github.com/fvwmorg/fvwm3/releases/%{version}/%{srcname}-%{version}.tar.gz

#block-logo
Source1:        fvwm3.png
#minimal system-wide config to be installed as system.fvwm2rc
Source2:        system-minimal.fvwm3rc
#minimal configuration file, called from the system-minimal.fvwm2rc
Source3:        fvwm3rc-minimal.mga

# to get an icon on the xterm button
Source6:        fvwm3_terminal.png

#enhanced config files for mageia default settings
Source7:        system-mageia.fvwm3rc
Source8:        fvwm3rc-extra.mga
Source9:        fvwm3.desktop

#This patch changes the configuration file to be *.fvwm3rc (the
#default is .fvwm2rc) which is problematic for mga as we have fvwm2 as
#well, plus configuration files between the two versions are not
#compatible
Patch0:         fvwm3-1.1.0-fvwm3rc.patch


BuildRequires:  flex
BuildRequires:  sharutils
BuildRequires:  xsltproc
#BuildRequires:  golang
BuildRequires:  pkgconfig(pkg-config)
BuildRequires:  pkgconfig(libbson-1.0)
BuildRequires:  pkgconfig(libevent)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xpm)
BuildRequires:  pkgconfig(imlib2)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(xtrans)
BuildRequires:  readline-devel
BuildRequires:  ruby-asciidoctor

#BuildRequires:  pkgconfig(tinfo)
#BuildRequires:  libstroke-devel
#BuildRequires:  pkgconfig(librsvg-2.0)
#BuildRequires:  pkgconfig(xinerama)



# for fvwm-menu-headlines
Requires:       desktop-common-data
# for fvwm-menu-xlock
Requires:       xlockmore
# for doing something
Requires:       xterm
# for iconification and wallpaper
Requires:       xwd
Requires:       imagemagick
Requires:       feh
# for mimeinfo
Requires:       perl-File-MimeInfo
# for compositing (enhancement only)
Recommends:       xcompmgr
Recommends:       transset-df

Conflicts:        fvwm2

Requires:         %{name}-doc

Requires(post):      update-alternatives
Requires(postun):    update-alternatives
Requires(posttrans): update-alternatives


%description
Fvwm3 is a multiple large virtual desktop window manager, originally
(a looooong time ago, 1993!) derived from twm. Shortly, it is the successor
to fvwm2. Fvwm3 is intended to have a small memory footprint but a
rich feature set, be extremely customizable and extendible, and have a
high degree of Motif mwm compatibility. Currently, your existing fvwm2
config will work with fvwm3.




%package -n %{cfgname}
Summary:        Mageia system-wide configuration for Fvwm3
Group:          Graphical desktop/Other
Requires:       fvwm3
#for button bar
Requires:       wmcalclock
Requires:       wmtop
%ifarch %{ix86} x86_64
Requires:       wmcpufreq
%endif
Requires:       wmforkplop
Requires:       wmhdplop
Requires:       wmbutton
Requires:       wmmoonclock
Requires:       wmsystemtray
# for the menu
Requires:       rxvt-unicode
Recommends:     terminology
# for fvwm-bug
Recommends:     sendmail-command

Requires(post):      update-alternatives
Requires(postun):    update-alternatives

%description -n %{cfgname}
%{summary}.


%package -n %{docname}
Summary:        Documentation files for Fvwm3
Group:          Graphical desktop/Other
Conflicts:      fvwm2-doc

%description -n %{docname}
%{summary}.


%prep
%setup -q -n %{srcname}-%{version}
%autopatch -p1
autoreconf -fi


%build
%configure \
    --enable-mandoc \
    --sysconfdir=%{fvwmconfdir} \
    --with-imagepath=%{_datadir}/icons \
    --disable-golang

%make_build LOCALEDIR=%{_datadir}/locale localedir=%{_datadir}/locale



%install
%{make_install} LOCALEDIR=%{_datadir}/locale localedir=%{_datadir}/locale

install -D -m644 %{SOURCE1} %{buildroot}%{_iconsdir}/fvwm3.png
install -D -m644 %{SOURCE2} %{buildroot}%{fvwmconfdir}/system-minimal.fvwm3rc
install -D -m644 %{SOURCE3} %{buildroot}%{fvwmconfdir}/fvwm3rc-minimal.mga

install -D -m644 %{SOURCE6} %{buildroot}%{_iconsdir}/fvwm3_terminal.png
install -D -m644 %{SOURCE7} %{buildroot}%{fvwmconfdir}/system-mageia.fvwm3rc
install -D -m644 %{SOURCE8} %{buildroot}%{fvwmconfdir}/fvwm3rc-extra.mga

install -D -m644 %{SOURCE9} %{buildroot}%{_datadir}/xsessions/fvwm3.desktop


%find_lang %{name} --all-name


%files -f %{name}.lang
%doc NEWS COPYING
%config(noreplace) %{fvwmconfdir}/fvwm3rc-minimal.mga
%config(noreplace) %{fvwmconfdir}/system-minimal.fvwm3rc
%{_bindir}/*
%{_libexecdir}/%{name}
%{_datadir}/xsessions/fvwm3.desktop
%{_datadir}/%{name}
%{_iconsdir}/fvwm3.png
%{_mandir}/man1/fvwm3*




%post
#if the file has been edited, or so, it is a regular file
#and not a symlink. So we first rename it before calling
#update-alternatives to create the symlink.
if [ -f %{fvwmconfdir}/system.fvwm3rc -a ! -h %{fvwmconfdir}/system.fvwm3rc ]; then
    mv %{fvwmconfdir}/system.fvwm3rc %{fvwmconfdir}/system.fvwm3rc.rpmold
fi
update-alternatives --install %{fvwmconfdir}/system.fvwm3rc fvwm3-config \
                    %{fvwmconfdir}/system-minimal.fvwm3rc 10

%postun
#uninstall only
if [ $1 -eq 0 ]; then
   update-alternatives --remove fvwm3-config %{fvwmconfdir}/system-minimal.fvwm3rc
fi

%posttrans
#old releases had system.fvwm3rc as file packaged in, so our symlink
#will be removed if one upgrade from those.
if ! [ -h %{fvwmconfdir}/system.fvwm3rc ]; then
   update-alternatives --install %{fvwmconfdir}/system.fvwm3rc fvwm3-config \
                    %{fvwmconfdir}/system-minimal.fvwm3rc 10
fi

# (ovitters) In posttrans, $1 is always equal to 1, even in the upgrade case.
# So just run this always:
if [ -e %{_datadir}/xsessions/09Fvwm3.desktop ]; then
        rm -rf %{_datadir}/xsessions/09Fvwm3.desktop
fi
if [ -e %{_sysconfdir}/X11/dm/Sessions/09Fvwm3.desktop ]; then
        rm -rf %{_sysconfdir}/X11/dm/Sessions/09Fvwm3.desktop
fi



%files -n %{cfgname}
%config(noreplace) %{fvwmconfdir}/fvwm3rc-extra.mga
%config(noreplace) %{fvwmconfdir}/system-mageia.fvwm3rc
%{_iconsdir}/fvwm3_terminal.png

%post -n %{cfgname}
if [ -f %{fvwmconfdir}/system.fvwm3rc -a ! -h %{fvwmconfdir}/system.fvwm3rc ]; then
    mv %{fvwmconfdir}/system.fvwm3rc %{fvwmconfdir}/system.fvwm3rc.rpmold
fi
update-alternatives --install %{fvwmconfdir}/system.fvwm3rc fvwm3-config \
                    %{fvwmconfdir}/system-mageia.fvwm3rc 11

%postun -n %{cfgname}
if [ $1 -eq 0 ]; then
   update-alternatives --remove fvwm3-config %{fvwmconfdir}/system-mageia.fvwm3rc
fi


# These files conflicts with those of fvwm2 (and are the same), let's
# put them in a conflicting separate package
%files -n %{docname}
%{_mandir}/man1/Fvwm*
%{_mandir}/man1/fvwm-*
