%define         srcname        fvwm3
%define         cfgname        %{name}-config-mageia
%define         fvwmconfdir    %{_sysconfdir}/fvwm3
%define         docname        %{name}-doc

Name:           fvwm3
Version:        1.1.4
Release:        1
Summary:        FVWM version 3, the successor to fvwm2 
License:        GPLv2+
Group:          Graphical desktop/Other

URL:            https://www.fvwm.org/
Source0:        https://github.com/fvwmorg/fvwm3/releases/%{version}/%{srcname}-%{version}.tar.gz
Source1:        fvwm3.png
Source9:        fvwm3.desktop

BuildRequires:  meson
BuildRequires:  flex
BuildRequires:  sharutils
BuildRequires:  xsltproc
#BuildRequires:  golang
BuildRequires:  pkgconfig(pkg-config)
#BuildRequires:  pkgconfig(libbson-1.0)
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
BuildRequires:  asciidoctor

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
Recommends:       feh
# for mimeinfo
# broken, so no
#Requires:       perl-File-MimeInfo
# for compositing (enhancement only)
Recommends:       xcompmgr
Recommends:       transset-df
Recommends:       rxvt-unicode
Recommends:     terminology

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

%package -n %{docname}
Summary:        Documentation files for Fvwm3
Group:          Graphical desktop/Other
Conflicts:      fvwm2-doc

%description -n %{docname}
%{summary}.


%prep
%autosetup -n %{srcname}-%{version} -p1


%meson \
        -Dxpm=enabled \
        -Dxrender=enabled \
        -Dxfixes=enabled \
        -Dxcursor=enabled \
        -Dsvg=enabled \
        -Dsm=enabled \
        -Dreadline=enabled \
        -Dpng=enabled \
        -Dlibsvg-cairo=enabled \
        -Dfreetype=enabled \
        -Dbidi=enabled
        -Dgolang=disabled \
        -Dmandoc=true \
        --sysconfdir=%{fvwmconfdir}
%build        
%meson_build

%install
#{make_install} LOCALEDIR=%{_datadir}/locale localedir=%{_datadir}/locale
%meson_install

install -D -m644 %{SOURCE1} %{buildroot}%{_iconsdir}/fvwm3.png

#install -D -m644 %{SOURCE6} %{buildroot}%{_iconsdir}/fvwm3_terminal.png

install -D -m644 %{SOURCE9} %{buildroot}%{_datadir}/xsessions/fvwm3.desktop


%find_lang %{name} --all-name


%files -f %{name}.lang
%doc NEWS COPYING
%{_bindir}/*
%{_libexecdir}/%{name}
%{_datadir}/xsessions/fvwm3.desktop
%{_datadir}/%{name}
%{_iconsdir}/fvwm3.png
%{_mandir}/man1/fvwm3*



%post
# (ovitters) In posttrans, $1 is always equal to 1, even in the upgrade case.
# So just run this always:
if [ -e %{_datadir}/xsessions/09Fvwm3.desktop ]; then
        rm -rf %{_datadir}/xsessions/09Fvwm3.desktop
fi
if [ -e %{_sysconfdir}/X11/dm/Sessions/09Fvwm3.desktop ]; then
        rm -rf %{_sysconfdir}/X11/dm/Sessions/09Fvwm3.desktop
fi

# These files conflicts with those of fvwm2 (and are the same), let's
# put them in a conflicting separate package
%files -n %{docname}
%{_mandir}/man1/Fvwm*
%{_mandir}/man1/fvwm-*
