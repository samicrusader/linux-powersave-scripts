# Scripts for controlling power on (Intel) Linux laptops

(credit to [Maythux](https://github.com/maythux) and [Ventto](https://github.com/Ventto))

I have an Acer Nitro 5 (AN515-53) running Arch Linux:
![](https://files.catbox.moe/teqbc3.png)

Having not opted to use any proper desktop environment, having some form of battery notification and power saving mechanism would have been great!

There's script that utilize notify-send to send notifications about your batteries state: [batify](https://github.com/Ventto/batify)

## The sadness

However, this relies entirely on your laptop actually sending the battery status to udev. Which mine does not.

For power-saving, a thing I wanted to do was to underclock my machine when the charger was unplugged. If I was to do anything intensive, I'd be plugged in anyways.

However, the intel_pstate driver would have said otherwise, likely because of how my laptop is.

This meant that I couldn't easily just call cpupower to change the governor from `powersave` to `performance` and vice-versa, as it did little to nothing.

For this to properly work, I'd have to set each thread to allow turbo boost. I had found a script to do so at [this AskUbuntu thread](https://askubuntu.com/questions/619875/disabling-intel-turbo-boost-in-ubuntu/619881#619881), and tweaked it to forcefully enable turbo after setting each thread.

This is a hacky solution, but it is what works for me, hence I'm publishing it here.

## Installation

This entirely assumes you use [systemd](https://systemd.io) as your init daemon, that you use [mkinitcpio](https://github.com/archlinux/mkinitcpio) to create your `initrd.img`, and that your CPU is from Intel and above like 6th gen or something.

* Install cpupower, [msr-tools](https://github.com/intel/msr-tools), and [xpub](https://github.com/Ventto/xpub). xpub will allow our script to send notifications to our X session.
* Include `msr` in your `initrd`'s `MODULES` (in `/etc/mkinitcpio.conf` for mkinitcpio).
* Tweak `capacity` and `charger` in [`battery-check.py`](battery-check.py) to match your laptop's battery and AC jack. You can also tweak the threshold for each notification, and eventual hibernation.
* Edit the path to [`battery-check.py`](battery-check.py) in the [`battery-check.service`](battery-check.service) unit file.
* Edit the path to [`turboctl.sh`](turboctl.sh) in both udev rules in [`rules.d/`](rules.d/).
* Copy `battery-check.service` to `/etc/systemd/system`.
* Enable and start `battery-check.service`.
* Restart your system to fully initialize the new udev rules.